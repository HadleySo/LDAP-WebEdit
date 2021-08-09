import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")


def main(request):
    print("INFO: Beginning to add entry to LDAP server")
    print(request.form)
    from . import searchLDAP, connections

    nameList = searchLDAP.getBaseName()

    # Connect and Bind to LDAP server
    conn = connections.connect()
    if conn == None:
        print("[ERROR] Search failed due to failed connection")
        addResult = [False, "[ERROR] Search failed due to failed connection"]
        return addResult
    bindResult = connections.bind(conn)
    if not (bindResult == None):
        connections.disconnect(conn)
        addResult = [False, bindResult]
        return addResult

    # Get BaseDN from config file
    baseDN = searchLDAP.getBaseDN()
    if baseDN == False:
        addResult = [False, "Unable to get Base DN. Most likely config error"]
        connections.disconnect(conn)
        return addResult

    # Set attributes based on form
    lName = request.form['lName']
    fName = request.form['fName']
    pNum = request.form['pNum']
    notes = request.form['notes']
    if len(notes) < 1:
        notes = ""
    else:
        notes = notes.replace("'", "")

    pNum = pNum.replace("'", "")
    fName = fName.replace("'", "")
    lName = lName.replace("'", "")

    dn = ""
    if request.form['addBase'] == 'baseOne':
        dn = baseDN[0]
    elif request.form['addBase'] == 'baseTwo':
        dn = baseDN[1]
    if dn == False:                                                 # When the DN selected does not exist tell user
        print("[ERROR] The Base DN you selected is not configured.")
        addResult = [
            False, "[ERROR] The Base DN you selected is not configured."]
        connections.disconnect(conn)
        return addResult

    # Create LDAP record Tuple
    dn = "cn=" + fName + "," + dn
    recordTup = (
        ('cn', bytes(fName, 'utf-8')),
        ('objectclass', bytes('person', 'utf-8')),
        ('sn', bytes(lName, 'utf-8')),
        ('description', bytes(notes, 'utf-8')),
        ('telephoneNumber', bytes(pNum, 'utf-8'))
    )

    print("The created recordTup:")
    print(recordTup)
    print("The requested DN:")
    print(dn)

    # Send to LDAP server
    try:
        conn.add_s(dn, recordTup)
        addResult = [True, lName + "\n" + fName +
                     "\n" + pNum + "\n" + notes + "\n" + dn]
        connections.disconnect(conn)
        return addResult
    except Exception as e:
        print("[ERROR] Unable to add entry after creating recordTupple " + str(e))
        addResult = [
            False, "[ERROR] Unable to add entry after creating recordTupple. " + str(e)]
        connections.disconnect(conn)
        return addResult
