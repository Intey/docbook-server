import React from 'react'
import {connect} from 'react-redux'
import { createDateElement, generateXML, loadFormMapFromXML } from 'utils'
import 'jquery'
import 'bootstrap'
import URLS from 'api'

export default class App extends React.Component {
    constructor(props)
    {
      super(props)
      this.state = {
        inputType: "form",
        selectedType: "save"
      }
    }

    parseForm = (formElements) => {
      let inputs = Array.from(formElements)
        .filter( e => e.type != 'submit' && e.type != 'button' )
      return inputs.reduce( (acc, e) => {
        // skip no named
        if (!e.name) { 
          console.log("e name is empty", e)
          return acc
        }
        acc[e.name] = e.value
        return acc
      }, {})
    }

    saveXML = () => {
      // collectForm data
      let formMap = this.parseForm(document.querySelector('.form-horizontal'))
      let rootNode = generateXML(formMap)
      const newfile = 'data:application/octet-stream;charset=utf-8;base64,'
      const serializer = new XMLSerializer()
      const content = serializer.serializeToString(rootNode)
      window.open(newfile+btoa(content))
    }

    loadXML = () => {
      loadFormMapFromXML(null)
    }

    renderFileInputTab = () => {
      return (
        <form action={URLS.fromDate} method="post" className="form-horizontal" encType="multipart/form-data" >
          <div className="form-group">
            <input className="form-control" type="file" name="files[]" multiple/>
          </div>
          <div className="form-group">
            <input className="form-control btn-primary" type="submit" value="Upload"/>
          </div>
        </form>
      )
    }

    typeChange = (event) => {
      this.setState({selectedType: event.target.value})
    }

    formTypeTime = () => {
      switch(this.state.selectedType) {
        case 'save':
        case 'nosave':
          return (
            <div>
              <div className="form-group">
                <input className="form-control" type="date" name="from-date"/>
              </div>
              <div className="form-group">
                <input className="form-control" type="number" name="count" placeholder="количество дней отпуска"/>
              </div>
            </div>
          )
        case 'hours':
          return (
            <div>
              <div className="form-group">
                <input className="form-control" type="time" name="from-time"/>
              </div>
              <div className="form-group">
                <input className="form-control" type="time" name="to-time"/>
              </div>
            </div>
          )
        case 'move':
          return ( null ) 
        case 'empty':
          return ( null )
        default:
          break;
      }
    }

    renderFormInputTab = () => {
      return (
        <form action={URLS.formForm} method="post" className="form-horizontal">
          <div className="form-group">
            <label for="today-date">Сегодня</label>
            <input className="form-control" type="date" name="today-date"/>
          </div>
          <div className="form-group">
            <select defaultValue="save" className="form-control" name="stat-type" id="stat-type" onChange={this.typeChange}>
              <option value="save">оплачиваемый</option>
              <option value="nosave">за свой счет</option>
              <option value="hours">на пару часов</option>
              {/* <option value="move">перенос оплачиваемого</option> */}
              <option value="empty">пустое</option>
            </select>
          </div>
          <div className="form-group">
            <input className="form-control" type="text" name="username"   placeholder = 'Имя'/>
          </div>
          <div className="form-group">
            <input className="form-control" type="text" name="secondname" placeholder = 'Фамилия'/>
          </div>
          <div className="form-group">
            <input className="form-control" type="text" name="patronymic" placeholder = 'Отчество'/>
          </div>
          <div className="form-group">
            <input className="form-control" type="text" name="sector" placeholder="Сектор (например 01054-1)"/>
          </div>
          <div className="form-group">
            <input className="form-control" type="text" name="prof" placeholder="Профессия"/>
          </div>
          <div className="form-group">
            <input className="form-control" type="text" name="category" placeholder="Категория(Если есть)"/>
          </div>

          {this.formTypeTime()}

        <div className="form-group">
          <input className="form-control btn-primary" type="submit" value="Upload"/>
        </div>
        <div className="form-group">
          <button type="button" className="btn btn-default col-xs-6" onClick={this.saveXML}>Сохранить в XML</button>
          <button type="button" className="btn btn-default col-xs-6" onClick={this.loadXML}>Загрузить из XML</button>
        </div>
        </form>
      )

    }

    render() {
      let fileTab = this.renderFileInputTab()
      let formTab = this.renderFormInputTab()

      return (
        <div className="container">
          <ul className="nav nav-tabs" role="tablist">
            <li className="active" role="presentation">
              <a aria-controls="form" href="#form" role="tab" data-toggle="tab">Форма для заполнения</a>
            </li>
            <li role="presentation">
              <a aria-controls="form" href="#file" role="tab" data-toggle="tab">Файлом</a>
            </li>
          </ul>
          <div className="tab-content">
            <div id="form" className="tab-pane fade in active" role="tabpanel">
              <div className="container">
                {formTab}
              </div>
            </div>
            <div id="file" className="tab-pane fade" role="tabpanel">
              <div className="container">
                {fileTab}
              </div>
            </div>
          </div>
        </div>
      )
    }
}
