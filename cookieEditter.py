import re

'''
input (string)all cookies and return what i need is etutor Cookies
將整個cookie字串傳入 然後回傳 我所需要的etutor的部份的cookies
'''


def getEtutorCookies(input1):
    splitdot = input1.split(',')
    etutorCookieStrings = []
    for i in splitdot:
        if i[1] == 'M':
            etutorCookieStrings.append(i)

    # remove garbage info and put it into dict
    etutorCookies = []
    for i in etutorCookieStrings:
        cookieSplite = re.sub(";.*", ";", i)
        cookieSplite = cookieSplite.replace(" ", "")
        if re.search("deleted", cookieSplite) == None:
            etutorCookies.append(cookieSplite)

    return etutorCookies
