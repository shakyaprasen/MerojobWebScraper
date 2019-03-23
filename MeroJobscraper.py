#! python3
# lucky.py - Opens several Google search results.

import requests
import sys
import webbrowser
import bs4

jobNumber = 1


def getJobDetailSoup(url):
    print('......Getting job details from : ' + url + '......')
    detailRes = requests.get(url)
    detailRes.raise_for_status()

    return(bs4.BeautifulSoup(detailRes.text))


def writeLoop(soupTemp, file_object):
    global jobNumber
    inputEl = soupTemp.select('#search_job > .card.mt-3.hover-shadow')
    for index, job in enumerate(inputEl):
        print('Writing Job Number ' + str(jobNumber) + '......')
        file_object.write('\n')
        file_object.write('\n')
        file_object.write('Job number  ' + str(jobNumber) + ': \n')
        jobNumber += 1
        jobLink = job.find_all("a", class_="no-uline")[0].get('href')
        jobUrl = 'https://merojob.com' + jobLink
        file_object.write('link: ' + jobUrl)
        file_object.write('\n')
        jobInfo = job.stripped_strings
        for info in jobInfo:
            file_object.write(repr(info))
            file_object.write('\n')

        # Get and write details of job
        file_object.write('\n')
        file_object.write('Job Details: \n')
        jobDetailSoup = getJobDetailSoup(jobUrl)
        jobDetailSoup = jobDetailSoup.select('.card-header + .card-block')[0]
        for jobDetailSoup in jobDetailSoup.strings:
            file_object.write(repr(jobDetailSoup))
        file_object.write('\n')
        file_object.write('Details Finished \n')
        file_object.write('\n')

    return


def getSoup(page):
    print('......Getting page number: ' + str(page) + '......')
    res = requests.get('https://merojob.com/search/?q=' +
                       ' '.join(sys.argv[1:]) + '&page=' + str(page))
    res.raise_for_status()

    # Retrieve top search result links.
    return(bs4.BeautifulSoup(res.text))


print('Finding...')  # display text while downloading the Google page
soup = getSoup(1)

numberOfJobs = soup.select('#job-count')[0].stripped_strings
searchString = ''


for string in numberOfJobs:
    searchString += repr(string)

searchString = searchString.replace('\'', '')
totalJobs = searchString.split(' ')[-1]
print('Found Total Jobs: ' + totalJobs)

i = 0
numberOfLoops = int(totalJobs)//6

if int(totalJobs) % 6 > 0:
    numberOfLoops += 1

jobs = []

file_ob = open('jobsfrom_merojob_of_' + ' '.join(sys.argv[1:]), 'a')
writeLoop(soup, file_ob)


for times in range(1, numberOfLoops):
    newSoup = getSoup(times + 1)
    writeLoop(newSoup, file_ob)


file_ob.close()
