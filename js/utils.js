
export function createDateElement(createElement, dateString)
{
  let date = new Date(dateString)
  let today = createElement('today')
  let year = createElement('year')
  year.textContent = date.getFullYear()
  today.appendChild(year)
  let month = createElement('month')
  month.textContent = date.getMonth()
  today.appendChild(month)
  let day = createElement('day')
  day.textContent = date.getDay()
  today.appendChild(day)

  return today
}

// <root>
//   <type>save</type>
//   <today>
//     <year>2017</year>
//     <month>августа</month>
//     <day>10</day>
//   </today>
//   <time>
//     <from>
//       <year>2017</year>
//       <month>июня</month>
//       <day>01</day>
//       <hour>9</hour>
//       <minute>00</minute>
//     </from>
//     <count>14</count>
//   </time>
//   <sector>
//     <id>01054-1</id>
//     <iam>
//       <surname>Чурин</surname>
//       <name>Дмитрий</name>
//       <patronymic>Романович</patronymic>
//       <prof>инженер-программист</prof>
//       <cat>1</cat>
//     </iam>
//   </sector>
// </root>
export function generateXML(formMap)
{
  let doc = document.implementation.createDocument(null, "root");
  let rootNode = doc.children[0]

  const createElement = doc.createElement.bind(doc)
  let fromDate = createDateElement(createElement, formMap['from-date'])
  let today = createDateElement(createElement, formMap['today-date'])

  rootNode.appendChild(today)
  rootNode.appendChild(fromDate)
  const newfile = 'data:application/octet-stream;charset=utf-8;base64,'
  return rootNode
}

export function loadFormMapFromXML(filedata) 
{
  return {}
}
