heart = document.querySelector('#heart')
kidney = document.querySelector('#kidney')
liver = document.querySelector('#liver')
eye = document.querySelector('#eye')
lungs = document.querySelector('#lungs')
pancreas = document.querySelector('#pancreas')

const organ_url = '/update_organ_requirement'

heart.addEventListener('click', e => {
    const organ_name = "heart"
    fetch(organ_url, {
        body: JSON.stringify({
            organ: organ_name,
        }),
        method: 'POST'
    }).then(res => {
        res.json().then(data => console.log(data))
    })
})

kidney.addEventListener('click', e => {
    const organ_name = "kidney"
    fetch(organ_url, {
        body: JSON.stringify({
            organ: organ_name,
        }),
        method: 'POST'
    }).then(res => {
        res.json().then(data => console.log(data))
    })
})

liver.addEventListener('click', e=>{
    const organ_name = "liver"
    fetch(organ_url, {
        body: JSON.stringify({
            organ: organ_name,
        }),
        method: 'POST'
    }).then(res => {
        res.json().then(data => console.log(data))
    })
})

eye.addEventListener('click', e=>{
    const organ_name = "eye"
    fetch(organ_url, {
        body: JSON.stringify({
            organ: organ_name,
        }),
        method: 'POST'
    }).then(res => {
        res.json().then(data => console.log(data))
    })
})

lungs.addEventListener('click', e=>{
    const organ_name = "lungs"
    fetch(organ_url, {
        body: JSON.stringify({
            organ: organ_name,
        }),
        method: 'POST'
    }).then(res => {
        res.json().then(data => console.log(data))
    })
})

pancreas.addEventListener('click', e=>{
    const organ_name = "pancreas"
    fetch(organ_url, {
        body: JSON.stringify({
            organ: organ_name,
        }),
        method: 'POST'
    }).then(res => {
        res.json().then(data => console.log(data))
    })
})