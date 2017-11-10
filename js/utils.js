
export function createDateElement(doc, formMap)
{
  let date = new Date(formMap['from-date'])
  let today = doc.createElement('today')
  let year = doc.createElement('year')
  year.textContent = date.getFullYear()
  today.appendChild(year)
  let month = doc.createElement('month')
  month.textContent = date.getMonth()
  today.appendChild(month)
  let day = doc.createElement('day')
  day.textContent = date.getDay()
  today.appendChild(day)

  return today
}
