// Валидация инпутов
let validation_reg = /[^А-Яа-я]/g
let inputs = document.getElementsByClassName('validation')
for (let input of inputs) {
    input.oninput = function() {
        this.value = this.value.replace(validation_reg, '')
    }
}

let inputs_len_3 = document.getElementsByClassName('validate_3');
for (let input of inputs_len_3) {
    input.oninput = function() {
        this.value = this.value.replace(validation_reg, '')
        this.value = this.value.substr(0, 3)
    }
}

let inputs_len_1 = document.getElementsByClassName('validate_1');
for (let input of inputs_len_1) {
    input.oninput = function() {
        this.value = this.value.replace(validation_reg, '')
        this.value = this.value.substr(0, 1)
    }
}


// получение и отправка данных
const ws = new WebSocket(url='ws://fiveletters.ru/ws')

function getValueDataByElementChild(parent_inputs) {
    let data = []
    let inputs = parent_inputs.getElementsByClassName('text-field__input')
    for (let input of inputs) {
        data.push(input.value)
    }
    return data
}

function isNull(data) {
    for (let el in data) {
        for (let i of data[el]) {
            if (i != '') {return false}
        }
    }
    return true
}

function getAllDataFromInputs() {
    let no_letters = getValueDataByElementChild(document.querySelector('.no_letters'))
    let are_letters = getValueDataByElementChild(document.querySelector('.are_letters'))
    let not_in_place = getValueDataByElementChild(document.querySelector('.not_in_place'))
    let in_place = getValueDataByElementChild(document.querySelector('.in_place'))
    let data = {
        no_letters: no_letters,
        are_letters: are_letters,
        not_in_place: not_in_place,
        in_place: in_place,
    }
    if (isNull(data)) {return {action: 'create'}}
    return {action: 'game', data: data}
}

function isStart() {
    let main_content = document.querySelector('.main-content').classList
    if (main_content.contains('display-none')) {
        main_content.toggle('display-none')
        let greeting = document.querySelector('.greeting').classList
        greeting.toggle('display-none')
    }
}

ws.onmessage = function(event) {
    let data = JSON.parse(event.data)
    let parent = document.querySelector('.values_word')
    parent.innerHTML = ''
    if (data['words'].length == 0) {
        let word_none = 'Нет подходящих вариантов по вашему запросу'
        let word_p = document.createElement('p')
        word_p.textContent = word_none
        let word_none_2 = 'попробу изменить фильтр'
        let word_p_1 = document.createElement('p')
        word_p_1.textContent = word_none_2
        parent.appendChild(word_p)
        parent.appendChild(word_p_1)
    }
    for (let el of data['words']) {
        let word_p = document.createElement('p')
        word_p.textContent = el
        parent.appendChild(word_p)
    }
}


function send(data) {
    ws.send(JSON.stringify(data))
}

function createGame(event) {
    send(getAllDataFromInputs())
    isStart()
}


document.getElementById('create-game').addEventListener('click', createGame)
