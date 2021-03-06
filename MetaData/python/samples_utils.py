from optpars_utils import *

from das_cli import get_data as das_query

from pprint import pprint

import os,json,fcntl,sys
from parallel  import Parallel
from threading import Semaphore

# -------------------------------------------------------------------------------
def shell_expand(string):
    if string:
        return os.path.expanduser( os.path.expandvars(string) )
    return None


# -------------------------------------------------------------------------------
def ask_user(question,responses=["y","n"]):
    reply = None
    while not reply in responses:
        print "%s [%s]" % ( question, "".join(responses) ), 
        reply = raw_input()
    return reply

# -------------------------------------------------------------------------------
class SamplesManager(object):
    
    def __init__(self,
                 catalog,
                 cross_sections=["$CMSSW_BASE/src/flashgg/MetaData/data/cross_sections.json"],
                 dbs_instance="prod/phys03",
                 queue=None
                 ):
        """
        Constructur:
        @catalog: json file used to read/write dataset information
        @cross_sections: json file where samples cross sections are stored
        @dbs_instance: DBS instance tp use
        """
        self.cross_sections_ = {}
        self.dbs_instance_ = dbs_instance

        for xsecFile in cross_sections:
            fname = shell_expand(xsecFile)
            self.cross_sections_.update( json.loads( open(fname).read() ) )
            
        self.catalog_ = shell_expand(catalog)

        self.parallel_ = None
        self.sem_ = Semaphore()

        print "Will use the following datasets catalog:"
        print self.catalog_
        
        self.queue_ = queue
        
    def importFromDAS(self,list_datasets):
        """
        Import datasets from DAS to the catalog.
        @datasets: wildecard to be usd in dataset query
        """
        catalog = self.readCatalog()
        
        print "Importing from das %s" % list_datasets
        datasets = []
        for dataset in list_datasets:
            if "*" in dataset:
                response = das_query("https://cmsweb.cern.ch","dataset dataset=%s | grep dataset.name" % dataset, 0, 0, False, self.dbs_instance_)
        
                for d in response["data"]:
                    datasets.append( d["dataset"][0]["name"] )
            else:
                datasets.append(dataset)

        print "Datasets to import"
        print "\n".join(datasets)
        for dsetName in datasets:
            print "Importing %s" % dsetName
            files = self.getFilesFomDAS(dsetName)
            if dsetName in catalog:
                catalog[ dsetName ]["files"]  = files
            else:
                catalog[ dsetName ] = { "files" : files }
            
        print "Writing catalog"
        self.writeCatalog(catalog)
        print "Done"

    def getFilesFomDAS(self,dsetName):
        """
        Read dataset files from DAS.
        @dsetName: dataset name
        """
        response = das_query("https://cmsweb.cern.ch","file dataset=%s | grep file.name,file.nevents" % dsetName, 0, 0, False, self.dbs_instance_)
        
        files=[]
        for d in response["data"]:
            for jf in d["file"]:
                if "nevents" in jf:
                    files.append({ "name" : jf["name"], "nevents" : jf["nevents"] })
                    break
                ## files.append( { "name" : d["file"][0]["name"], "nevents" : d["file"][0]["nevents"] } )

        return files

    def importFromEOS(self,folders):
        """
        Import datasets from DAS to the catalog.
        @datasets: dataset to be imported
        """
        catalog = self.readCatalog()
        
        auto=False
        assumeOk=False
        for folder in folders:
            dsetName = ""

            print
            print "importing folder\n %s" % folder
            
            while not len(dsetName.split("/")) == 4:
                if auto:
                    splitFolder = folder.split("/")
                    prim, sec = splitFolder[-4:-2]
                    dsetName = "/%s/%s/USER" % (prim,sec)
                    print "guessed dataset name ", dsetName
                    if not assumeOk:
                        resp=ask_user("ok?",["y","n","a"])
                        if resp == "n":
                            dsetName = ""
                            auto=False
                        elif resp=="a":
                            assumeOk=True
                if not auto:
                    print "enter dataset name (auto/noauto to enables/disables automatic guessing) ",
                    dsetName = raw_input()
                    if(dsetName=="auto"):
                        auto=True
                    elif (dsetName=="noauto"):
                        auto=False
                
                
            print "Importing %s as %s" % (folder,dsetName)
            files = self.getFilesFomEOS(folder)            
            if dsetName in catalog:
                catalog[ dsetName ]["files"]  = files
            else:
                catalog[ dsetName ] = { "files" : files }
            
        print "Writing catalog"
        self.writeCatalog(catalog)
        print "Done"
        
    def getFilesFomEOS(self,dsetName):
        """
        Read dataset files crawling EOS.
        @dsetName: dataset name
        Note: not implemented
        """
        
        if not self.parallel_:
            self.parallel_ = Parallel(200,self.queue_)
        
        ret,out = self.parallel_.run("/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select",["find",dsetName],interactive=True)[2]
        ## print out
        files = []
        for line in out.split("\n"):
            if line.endswith(".root"):
                files.append( {"name":line.replace("/eos/cms",""), "nevents":0} )

        return files

    def findDuplicates(self,dsetName):
        """
        Find duplicate job outputs in dataset.
        @dsetName: dataset name
        Note: not implemented
        """
        pass
    
    def invalidateBadFiles(self,dsetName):
        """
        Invalidate duplicate job output and corrupted files in DAS.
        @dsetName: dataset name
        Note: not implemented
        """
        pass

    def checkAllDatasets(self):
        """
        Look for corrupted files in the whole catalog.
        """
        catalog = self.readCatalog()
        
        self.parallel_ = Parallel(50,self.queue_)
        ## self.parallel_ = Parallel(1,self.queue_)

        print "Checking all datasets"
        for dataset in catalog.keys():            
            self.checkDatasetFiles(dataset,catalog)
        
        outcomes = self.parallel_.wait(printOutput=False)

        ## for dsetName,ifile,fName,ret,out in outcomes:
        for ign1, ign2, outcome in outcomes:
            dsetName,ifile,fName,ret,out = outcome
            info = catalog[dsetName]["files"][ifile]
            if info["name"] != fName:
                print "Inconsistent outcome ", info["name"], dsetName,ifile,fName,ret,out
            else:
                if ret != 0:
                    info["bad"] = True
                else:
                    extraInfo = json.loads(str(out))
                    for key,val in extraInfo.iteritems():
                        info[key] = val

        print "Writing catalog"
        self.writeCatalog(catalog)
        print "Done"
    
    def checkDatasetFiles(self,dsetName,catalog=None):
        """
        Look for corrupted files in dataset.
        @dsetName: dataset name
        Note: not implemented
        """
        writeCatalog = False
        if not catalog:
            catalog = self.readCatalog()
            writeCatalog = True
        
        wait = False
        if not self.parallel_:
            self.parallel_ = Parallel(16,self.queue_)
            wait = True

        print 
        print "Checking dataset",dsetName
        info = catalog[dsetName]
        files = info["files"]
        print "Number of files: ", len(files)
        
        toremove = []
        for ifil,eifil in enumerate(files):
            if ifil in toremove:
                continue
            for jfil,ejfil in enumerate(files[ifil+1:]):
                if ifil+jfil in toremove:
                    continue
                if eifil["name"] == ejfil["name"]:
                    toremove.append(ifil)
                else:
                    iid = eifil["name"].rstrip(".root").rsplit("_",1)[-1]
                    jid = ejfil["name"].rstrip(".root").rsplit("_",1)[-1]
                    if iid == jid:
                        print "duplicated file index ", iid
                        print eifil["name"]
                        print ejfil["name"]
                        reply=ask_user("keep both? ")
                        if reply == "n":
                            if ask_user( "keep %s? " % ejfil["name"] ) == "n":
                                ## files.pop(ifil+jfil)
                                toremove.append(ifil+jfil)
                            if ask_user( "keep %s? " % eifil["name"] ) == "n":
                                toremove.append(ifil)
                                ## files.pop(ifil)
                                
        for ifile in sorted(toremove,reverse=True):
            ## print ifile
            files.pop(ifile)
            
        print "After duplicates removal: ", len(files)
        info = catalog[dsetName]["files"] = files
        for ifile,finfo in enumerate(files):            
            name = finfo["name"]
            self.parallel_.run(SamplesManager.checkFile,[self,name,dsetName,ifile])

        if wait:
            self.parallel_.wait(printOutput=False)            
            self.parallel_ = None
            
        if writeCatalog:
            self.writeCatalog(catalog)

    def reviewCatalog(self):
        datasets,catalog = self.getAllDatasets()

        primaries = {}
        keepAll = False
        for d in datasets:
            if not keepAll:
                reply = ask_user("keep this dataset (yes/no/all)?\n %s\n" % d, ["y","n","a"])
                if reply == "n":
                    catalog.pop(d)
                    continue
                if reply == "a": 
                    keepAll = True
            primary = d.split("/")[1]
            if not primary in primaries:
                primaries[ primary ] = []
                
            primaries[ primary ].append(d)
            
        for name,val in primaries.iteritems():
            if len(val) == 1: continue
            reply = ask_user("More than one sample for %s:\n %s\nKeep all?" % (name,"\n ".join(val)),["y","n","m"])
            if reply == "m":
                dst = val[0]
                for merge in val[1:]:
                    self.mergeDataset(catalog[dst],catalog[merge])
                    catalog.pop(merge)
            if reply == "n":
                for d in val:
                    reply = ask_user("keep this dataset?\n %s\n" % d)
                    if reply == "n":
                        catalog.pop(d)
           
        self.writeCatalog(catalog)
        
    def mergeDataset(self,dst,merge):
        dstFiles=dst["files"]
        mergeFiles=merge["files"]
        for fil in mergeFiles:
            skip = False
            for dfil in dstFiles:
                if dfil["name"] == fil["name"]:
                    skip = True
            if not skip:
                dstFiles.append( fil )
        
    def checkFile(self,fileName,dsetName,ifile):
        """
        Check if file is valid.
        @fileName: file name
        """
        ## fName = "root://eoscms//eos/cms%s" % fileName
        fName = fileName
        tmp = ".tmp%s_%d.json"%(dsetName.replace("/","_"),ifile)
        ## print "fggCheckFile.py",[fName,tmp,"2>/dev/null"]
        ret,out = self.parallel_.run("fggCheckFile.py",[fName,tmp,"2>/dev/null"],interactive=True)[2]
        
        try:
            fout = open(tmp)
            out = fout.read()
            fout.close()
        except IOError, e:
            print ret, out 
            print e
            out = "{}"

        os.remove(tmp)
        return dsetName,ifile,fileName,ret,out
    
    
    def lockCatalog(self):
        """
        Lock catalog file for writing.
        Note: not implemented.
        """
        pass
    
    def unlockCatalog(self):
        """
        Unlock catalog file for writing.
        Note: not implemented.
        """
        pass
    
    def readCatalog(self,throw=False):
        """
        Read catalog from JSON file.
        @throw: thow exception if file does not exists.
        """
        if os.path.exists(self.catalog_):
            return json.loads( open(self.catalog_).read() )
        if throw:
            raise Exception("Could not find dataset catalog %s" % ( self.catalog_ ))
        return {}
    
    def writeCatalog(self,content):
        """
        Write catalog to JSON file.
        @content: catalog content.
        """
        if not os.path.exists( os.path.dirname(self.catalog_) ):
            os.mkdir( os.path.dirname(self.catalog_) )

        with open(self.catalog_,"w+") as fout:
            fout.write( json.dumps(content,indent=4,sort_keys=True) )
            fout.close()
    
    def getDatasetMetaData(self,maxEvents,primary,secondary=None,jobId=-1,nJobs=0):
        """
        Extract dataset meta data.
        @maxEvents: maximum number of events to read.
        @primary: primary dataset name.
        @secondary: secondary dataset name.
        
        returns: tuple containing datasetName,cross-section,numberOfEvents,listOfFiles
        
        """
        catalog = self.readCatalog(True)
        primary = primary.lstrip("/")
        found = False
        xsec  = 0.
        allFiles = []
        totEvents = 0.
        totWeights = 0.
        for dataset,info in catalog.iteritems():
            empty,prim,sec,tier=dataset.split("/")
            if prim == primary:
                if secondary and sec != secondary:
                    continue
                if found:
                    raise Exception("More then one dataset matched the request: /%s/%s" % ( primary, str(secondary) ))
                found = dataset
                if prim in self.cross_sections_:
                    xsec = self.cross_sections_[prim]
                for fil in info["files"]:
                    if fil.get("bad",False):
                        continue
                    nev, name = fil["nevents"], fil["name"]
                    totEvents += nev
                    totWeights += fil.get("weights",0.)
                    allFiles.append(name)
                    if maxEvents > -1 and totEvents > maxEvents:
                        break
        if not found:
            raise Exception("No dataset matched the request: /%s/%s" % ( primary, str(secondary) ))
        
        if maxEvents > -1 and totEvents > maxEvents:
            totWeights = maxEvents / totEvents * totWeights
            totEvents = maxEvents
        maxEvents = int(totEvents)
        
        if totWeights != 0.:
            totEvents = totWeights
            
        if jobId != -1:
            files = [ allFiles[i] for i in range(jobId,len(allFiles),nJobs) ]
        else:
            files = allFiles

        return found,xsec,totEvents,files,maxEvents

    def getAllDatasets(self):
        catalog = self.readCatalog()
        datasets = sorted(catalog.keys())
        return datasets,catalog
    
    def clearCatalog(self):
        self.writeCatalog({})
    
# -------------------------------------------------------------------------------
class SamplesManagerCli(SamplesManager):
    
    def __init__(self,*args,**kwargs):

        commands = [ "",
                     "import                       imports datasets from DBS to catalog", 
                     "eosimport <list_of_folders>  imports datasets from EOS", 
                     "list                         lists datasets in catalog", 
                     "review                       review catalog to remove datasets", 
                     "check                        check files in datasets for errors and mark bad files"
                     ]
        
        parser = OptionParser(
            usage="""%%prog [options] <command> [[command2] [command3] ..]

Command line utility to handle FLASHgg samples catalog.

Commands:
%s
            """ % "\n   ".join(commands),
            option_list=[
                make_option("-V","--flashggVersion",
                            action="store", dest="flashggVersion", type="string",
                            default="*",
                            help="FLASHgg version to use (only relevant when importing). default: %default", 
                            ),
                make_option("-C","--campaign",
                            dest="campaign",action="store",type="string",
                            default="",
                            help="production campaign. default: %default",
                            ),
                make_option("-d","--dbs-instance",
                            dest="dbs_instance",action="store",type="string",
                            default="prod/phys03",
                            help="DBS instance to use. default: %default",
                            ),
                make_option("-m","--metaDataSrc",
                            dest="metaDataSrc",action="store",type="string",
                            default="flashgg",
                            help="MetaData package to use. default: %default",
                            ),
                make_option("--load",  # special option to load whole configuaration from JSON
                            action="callback",callback=Load(),dest="__opt__",
                            type="string",
                            help="load JSON file with configuration",metavar="CONFIG.json"
                            ),
                make_option("-q","--queue",
                            dest="queue",action="store",type="string",
                            default=None,
                            help="Run jobs in batch using specified queue. default: %default",
                            ),
                make_option("-v","--verbose",
                            action="store_true", dest="verbose",
                            default=False,
                            help="default: %default",)
                ]
                              )
        
        # parse the command line
        (self.options, self.args) = parser.parse_args()
        
    
    def __call__(self):
        
        (options,args) = (self.options,self.args)
    
        self.mn = SamplesManager("$CMSSW_BASE/src/%s/MetaData/data/%s/datasets.json" % (options.metaDataSrc,options.campaign),
                                 dbs_instance=options.dbs_instance)
        
        ## pprint( mn.cross_sections_ )
        if len(args) == 0:
            args = ["list"]
        
        method = getattr(self,"run_%s" % args[0],None)
        if not method:
            sys.exit("Unkown command %s" % a)
        if len(args)>1:
            method(*args[1:])
        else:
            method()
                
    def run_import(self,*args):
        if len(args)>0:
            print args
            self.mn.importFromDAS(list(args))
        else:
            self.mn.importFromDAS(["/*/*%s-%s*/USER" % (self.options.campaign,self.options.flashggVersion)])
    
    def run_eosimport(self,*args):
        self.mn.importFromEOS(args)
        
    def run_check(self):
        self.mn.checkAllDatasets()
    
    def run_list(self):
        datasets,catalog = self.mn.getAllDatasets()
        ## datasets = [ d.rsplit("/",1)[0] for d in datasets ]
        maxSec = 50
        halfSec = maxSec / 2
        firstHalf = halfSec - 1
        secondHalf = maxSec - halfSec - 1
        slim_datasets = []
        for d in datasets:
            empty,prim,sec,tier = d.split("/")
            if len(sec) > maxSec:
                sec = sec[0:firstHalf]+".."+sec[-secondHalf:-1]
            slim_datasets.append("/%s/%s/%s" % ( prim, sec, tier ) )
        ## datasets = slim_datasets
        ## largest = max( [len(d) for d in datasets] )
        totev = 0.
        totwei = 0.
        totfiles = 0
        largest = max( [len(d) for d in slim_datasets] )
        print
        print "Datasets in catalog:"
        print "-"*(largest+37)
        print "Name".ljust(largest), ("Num. events").rjust(11), ("Num. files").rjust(11), ("Avg weight").rjust(11)
        print "-"*(largest+37)
        for d,n in zip(datasets,slim_datasets):
            nevents = 0.
            weights = 0.
            nfiles = len(catalog[d]["files"])
            for fil in catalog[d]["files"]:
                nevents += fil.get("nevents",0.)
                weights += fil.get("weights",0.)
            print n.ljust(largest), ("%d" % int(nevents)).rjust(11), ("%d" % nfiles).rjust(11),
            if weights != 0.: print ("%1.2g" % ( weights/nevents ) ).rjust(11)
            else: print
            totev += nevents
            totwei += weights
            totfiles += nfiles
        print "-"*(largest+37)
        print "total".rjust(largest), ("%d" % int(totev)).rjust(11), ("%d" % totfiles).rjust(11)
        
    def run_clear(self):
        self.mn.clearCatalog()
    
    def run_review(self):
        self.mn.reviewCatalog()
