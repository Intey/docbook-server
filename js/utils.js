
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
