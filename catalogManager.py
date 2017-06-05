"""
Question: how to control the behavior when the we need to change the next block (when space of current block is not enough)
"""
import bufferManager
import json
"""
bytes to string : btyes.decode()
string to bytes: str.encode()
len(str)
"""
"""
todo:
is "No." necessary in this module?YES
YES it is useful when we try to delete one table (use No to locate the index of that table....)
So add No. to where it should be
-----------NO we can delete it in dict and convert to list at the end of the program
So not to remove now,,,, maybe it is useful in future


"""
"""
```json
tablesInfo[tableName]={
'primaryKey':
'size'*:
'fields'**:{
'type':
'typeParam':
'unique':
'index'*:str(indexName) or None}
}
```
"""
def openCatelog():
    # simple method from json file to dict
    try:
        with open('tableCatalog.txt','r') as infile:
            tablesInfo=json.load(infile)
        with open('indexCatalog.txt','r') as infile:
            indicesInfo=json.load(infile)
    except IOError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    return
    # ORIGINAL method: useful for other managers
    # try:
    #     f=open("tableCatalog.txt",'r')
    #     tablesBlockList=f.read().split()
    #     f.close()
    # except IOError:
    #     pass
    # try:
    #     f=open("indexCatalog.txt",'r')
    #     indicesBlockList=f.read().split()
    #     f.close()
    # except IOError:
    #     pass
    return
def closeCatelog():
    # from tablesInfo(dict) to json
    with open("tableCatalog.txt",'w') as outfile:
        json.dump(tablesInfo,outfile)
    with open("indexCatalog.txt",'w') as outfile:
        json.dump(indicesInfo,outfile)
    # for key,value in dict.items(tablesInfo):
    #     No,numOfColumns,primaryKeyName=value[0:3]
    #     tableName=key
    #     fields=[]
    #     for key2,value2 in dict.items(value[3]):
    #         fields+=[key2,str(value2[0]),str(value2[1],str(value2[2]))]
    #     tablesBlockList+=([str(No),str(True),tableName,str(numOfColumns),primaryKeyName]+fields)
    # f=open("tableCatalog.txt",'w')
    # f.write(' '.join(tablesBlockList))
    # f.close()
    # for key,value in dict.items(tablesInfo):
    #     No=value[0]
    #     indexName=key
    #     tableName,columnName=value[1:3]
    #     validation='True'
    #     indicesBlockList+=([str(No),validation,indexName,tableName,columnName])
    # f=open("indexCatalog.txt",'w')
    # f.write(' '.join(indicesBlockList))
    # f.close()
    # return
def tableListToDictValue(data):
    """
    given a data[] of one table, return a formatted tableInfoValue
    """
    No=int(data[0])
    validation=bool(data[1])
    numOfColumns=int(data[3])
    if not validation:
        return None
    tableInfoValue=[No,numOfColumns,data[4]]
    j=0
    column={}
    while j<numOfColumns:
        j+=1
        column[data[1+4*j]]=[int(data[4*j+2]),bool(data[4*j+3]),bool(data[4*j+4])]
    tableInfoValue.append(column)
    return tableInfoValue
def indexListToDictValue(data):
    validation=bool(data[1])
    if not validation:
        return None
    else:
        return [int(data[0]),data[3],data[4]]#No,tableName,columnName
def tableDictToStr(tableName,tableInfoValue):
    numOfColumns=tableInfoValue[1]
    table1=[str(tableInfoValue[0]),'1',tableName,str(numOfColumns),tableInfoValue[2]]
    table2=[]
    for key,value in dict.items(tableInfoValue[3]):
        table2+=([key,str(value[0]),str(value[1]),str(value[2])])
    return table1+table2
def extend(tableName,primaryKey,fields):
    value={}
    value['primaryKey']=primaryKey
    value['fields']={}
    size=4
    for item in fields:
        if(item['type']=='char'):
            size+=item['typeParam']
        else:
            size+=4 # float or int
        value['fields'][item['name']]={
        'type':item['type'],
        'typeParam':item['typeParam'],
        'unique':item['unique'],
        'index':None
        }
    value['size']=size
    return value
# def convertIn(fields):
#     myFields={}
#     for item in fields:
#         value=[-1,True,False]
#         if(item['type']=='float'):
#             value[0]=0
#         elif(item['type']=='char'):
#             value[0]=item['typeParam']['maxLength']
#         value[1]=item['unique']
#         myFields[item['name']]=value
#     return myFields
# def convertOut(tableName, primaryKeyName, fields):
#     newFields=[]
#     for key,value in dict.items(fields):
#         temp={}
#         temp['name']=key
#         if(value[0]==-1):
#             temp['type']='int'
#             temp['typeParam']={'maxLength':None}
#         elif(value[0]==0):
#             temp['type']='float'
#             temp['typeParam']={'maxLength':None}
#         else:
#             temp['type']='char'
#             temp['typeParam']={'maxLength':value[0]}
#         temp['unique']=value[1]
#         newFields.append(temp)
#     return {
#     'tableName':tableName,
#     'fields':newFields,
#     'primaryKey':primaryKeyName
#     }
def createTable(tableName,primaryKey,fields):
    """
    :param tableName:
    :param primaryKeyName:
    :param fields:{columnName:[int(type),bool(unique)],bool(index)}(type: -1:int,0:float,1~255:char(1~255))
    :return:successful or not
    this function should record
        the tableName,
        number of columns,
        name & type of columns,
        primary key,
        unique key,
        the name of column that has index & indexName
    """
    global numOfTables,tablesBlockList
    myFields=extend(tableName,primaryKey,fields)
    # add to dict
    # dict merge
    # for key in myFields:
    #     myFields[key].append(False)
    tablesInfo[tableName]=myFields
    numOfTables+=1
    # add to file
    # NO need anymore
    # tablesBlockList+=tableDictToStr(tableName,tablesInfo[tableName])
    # write list
    addIndexRecord(''.join(['index_',primaryKey]),tableName,primaryKey)
    return True
def dropTable(tableName):
    """
    :param tableName:
    :return: successful or not

    delete all the record of this table
    """
    # delete all the index
    for columnName, columnInfo in dict.items(tablesInfo[tableName]['fields']):
        indexName=columnInfo['index']
        if(indexName is not None):
            dropIndexRecord(indexName)
    # delete table
    tablesInfo.pop(tableName)
    return True
def findTable(tableName):
    """
    :param tableName:
    :return: {tableName:xxx,No:xxx,numOfColumns:xxx,etc}

    give tableName, return the information of the table
    """
    if(tableName in tablesInfo):
        infoList=tablesInfo[tableName]
        return {'tableName':tableName,'No':infoList[0],'numOfColumns':infoList[1],\
        'column':infoList[3],'primaryKeyName':infoList[2]}
    else:
        return None
def valueValidation(tableName,row):
    """
    check whether this row is valid for this table
    """
def getIndexName(tableName,columnName):
    """
    give tableName&columnName, return indexName if there is index(else return '')
    """
    indexName=''
    return indexName
def getTableAndColumnName(indexName):
    """
    give indexName, return [tableName,columnName]
    """
    return [indicesInfo[indexName]['tableName'],indicesInfo[indexName]['columnName']]
def addIndexRecord(indexName,tableName, columnName):
    # add to dict
    global numOfIndices,indicesBlockList
    indicesInfo[indexName]={
    'tableName':tableName,
    'columnName':columnName
    }
    # add to list
    numOfIndices+=1
    # update tablesInfo
    tablesInfo[tableName]['fields'][columnName]['index']=indexName
    return True
def dropIndexRecord(indexName):
    # pop in indicesInfo
    tableName,columnName=getTableAndColumnName(indexName)
    indicesInfo.pop(indexName)
    # reset None in tablesInfo
    tablesInfo[tableName]['fields'][columnName]['index']=None
    return True
def getAllColumn(tableName):
    columnList=[]
    return columnList
def getTableSize(tableName):
    """
    :param tableName:
    :return: the number of bytes of one row of record
    """
    return size
# DEBUG
tablesBlockList=[]#blocks of str type
tablesInfo={}#{tableName:[No,numOfColumns,primaryKeyName,{columnName:[type,unique,index]}]}
indicesBlockList=[]
indicesInfo={}#{indexName:[No, tableName,columnName]}
numOfTables=0
numOfIndices=0
"""
file format of recordCatalog.txt:
(totalLength:5+4*(numOfColumns))
[0]:No.
[1]:bool validation,# set when deleted
[2]:str tableName,
[3]:int numOfColumns,
[4]:str primaryKeyName;
[5+4*i]str columnName+type+unique?+index?[numOfColumns],
"""
#initialize tablesBlockList
openCatelog()
# ORIGINAL method (useful in other managers)
# i=0
# length=len(tablesBlockList)
# # initialize tablesInfo
# while i<length:
#     numOfColumns=int(tablesBlockList[i+3])
#     temp=tableListToDictValue(tablesBlockList[i:i+5+4*numOfColumns])
#     if temp is None:
#         i+=(5+4*numOfColumns)
#     else:
#         tablesInfo[tablesBlockList[i+2]]=temp
#         i+=(5+4*numOfColumns)
#         numOfTables+=1
# # initialize indicesBlockList
# """
# file format of indexCatalog.txt:
# [0]:int No,
# [1]:bool validation,
# [2]:str indexName,
# [3]:str tableName,
# [4]:str columnName;
# """
# i=0
# length=len(indicesBlockList)
# # initialize indicesInfo
# while i<length:
#     temp=indexListToDictValue(indicesBlockList[i:i+5])
#     if temp is None:
#         i+=5
#     else:
#         indicesInfo[indicesBlockList[i+2]]=temp#No,tableName,columnName
#         i+=5
#         numOfIndices+=1
# tablesBlockList=[]# can we put this line after we read it to dict in __init__()????? (save memory)
# indicesBlockList=[]# can we put this line after we read it to dict in __init__()????? (save memory)

if __name__=='__main__':
    tableName='student'
    primaryKey='sno'
    fields=[{'name': 'sno', 'type': 'char', 'unique': False, 'typeParam': 8}, {'name': 'sname', 'type': 'char', 'unique': True, 'typeParam': 16}, {'name': 'sage', 'type': 'int', 'unique': False, 'typeParam': None}, {'name': 'sgender', 'type': 'char', 'unique': False, 'typeParam': 1}]
    createTable(tableName,primaryKey,fields)
    # dropTable('student')
    closeCatelog()
