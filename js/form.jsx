import React from 'react'

export default class Form extends React.Component {
    render() {
        return (
        <div className="row">
            <form method="post" encType="multipart/form-data" >
                <input className="form-control" type="file" name="file" multiple/>
                <input className="form-control" type="submit" value="Upload"/>
            </form>
        </div>
        )
    }
}
