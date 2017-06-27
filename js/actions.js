function startFetchData() {
    return {
        type: 'start_fetch'
    }
}

function gotData(data) {
    return {
        type: 'response',
        payload: data
}
