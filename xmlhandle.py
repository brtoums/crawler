import xml.dom.minidom as minidom 
import codecs
import os
def makeXmlTag(path,type='text',clear = False,**kw):
	if  os.path.exists('task.xml') and clear==False: 
		dom = minidom.parse('task.xml')
		root = dom.documentElement
		for (k,v) in kw.items():
			value = str(v)
			if  value.find(']]>') > -1:
				type = 'text'
			if type == 'text':
				value = value.replace('&', '&amp;')
				value = value.replace('<', '&lt;')
				text = dom.createTextNode(value)
			elif type == 'cdata':
				text = dom.createCDATASection(value)
			ll = [ nodename.nodeName for nodename in root.childNodes]
			if k in ll:
				tag = dom.createElement(k)
				tag.appendChild(text)
				root.replaceChild(tag,root.getElementsByTagName(k)[0])

			else:
				tag = dom.createElement(k)
				tag.appendChild(text)
				root.appendChild(tag)
					# break	
	else:
		impl = minidom.getDOMImplementation()
		dom = impl.createDocument(None, 'lastask', None)
		root = dom.documentElement
		
		for (k,v) in kw.items():
			value = str(v)
			if  value.find(']]>') > -1:
				type = 'text'
			if type == 'text':
				value = value.replace('&', '&amp;')
				value = value.replace('<', '&lt;')
				text = dom.createTextNode(value)
			elif type == 'cdata':
				text = dom.createCDATASection(value)
			tag = dom.createElement(k)
			tag.appendChild(text)
			root.appendChild(tag)
			root.toprettyxml()
	with open(path, 'wb') as f:
		writer = codecs.lookup('utf-8')[3](f)
		dom.writexml(writer, encoding='utf-8')
		writer.close()
# list = [{'rowid':143},{'category':'分类'},{'title':'章节标题'},{'url':'http://url'},{'pageurl':'None'},]
# dics = {'rowid':14555,'category':'分类','title':'章节标题','url':'http://url','pageurl':'None'}
# dics = {'title':'章节标题'}
# path = 'task.xml'
# makeXmlTag(path,clear=True,**dics)
def readXml():
	dom = minidom.parse('task.xml')
	root = dom.documentElement
	children=root.childNodes
	info = {}
	for i in children:
		info[i.nodeName] = i.firstChild.nodeValue
	return info
	
# readXml()
if __name__=='__main__':
    print(readXml())
	
	


