import xmltodict


# DataSet Class holds the information about each dataset paths
class DataSet:
    def __init__(self, name, bugReport):
        self.name = name
        self.bugReport = bugReport


#bug reports paths
aspectj = DataSet('aspectj', 'data/AspectJop.xml')


print(aspectj)

# Parsing Data Sets

class BugReport:
    """Class representing each bug report"""

    def __init__(self, id, bug_id, summary, description, report_time, report_timestamp, status, commit, commit_timestamp, files, result, output):
        self.id = id
        self.bug_id = bug_id
        self.summary = summary
        self.description = description
        self.report_time = report_time
        self.report_timestamp = report_timestamp
        self.status = status
        self.commit = commit
        self.commit_timestamp = commit_timestamp
        self.files = files
        self.result = result
        self.output = output
        self.pos_tagged_summary = None
        self.pos_tagged_description = None
        self.pos_tagged_files = None


def getContent():
        with open('data/AspectJop.xml') as fd:
            doc = xmltodict.parse(fd.read())
            arr = []
            for i in doc["pma_xml_export"]["database"]["table"]:
                id = ''
                bug_id = ''
                summary = ''
                description = ''
                report_time = ''
                report_timestamp = ''
                status = ''
                commit = ''
                commit_timestamp = ''
                files = ''
                result = ''
                output = ''

                try:
                    id = i["column"][0]["#text"]
                except:
                    pass
                try:
                    bug_id = i["column"][1]["#text"]
                except:
                    pass
                try:
                    summary = i["column"][2]["#text"]
                except:
                    pass
                try:
                    description = i["column"][3]["#text"]
                except:
                    pass
                try:
                    report_time = i["column"][4]["#text"]
                except:
                    pass
                try:
                    report_timestamp = i["column"][5]["#text"]
                except:
                    pass
                try:
                    status = i["column"][6]["#text"]
                except:
                    pass
                try:
                    commit = i["column"][7]["#text"]
                except:
                    pass
                try:
                    commit_timestamp = i["column"][8]["#text"]
                except:
                    pass
                try:
                    files = i["column"][9]["#text"]
                except:
                    pass
                try:
                    result = i["column"][10]["#text"]
                except:
                    pass
                try:
                    output = i["column"][11]["#text"]
                except:
                    pass

                arr.append({"id": id, "bug_id": bug_id, "summary": summary, "description": description,
                            "report_time": report_time, "report_timestamp": report_timestamp, "status": status,
                            "commit": commit, "commit_timestamp": commit_timestamp, "files": files,
                            "result": result, "output": output})
            return arr


class Parser:
    def __init__(self, project):
        self.name = project.name
        self.bugReport = project.bugReport

    # Parse the xml files (Bug Reports)
    def parseBugReport(self):

        bug_reports = getContent()

        return bug_reports

