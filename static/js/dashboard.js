dashboard = document.querySelector("#dashboard")
about = document.querySelector("#about")
contact = document.querySelector("#contact")

li_d = document.querySelector("#li-dashboard")
li_a = document.querySelector("#li-about")
li_c = document.querySelector("#li-contact")

dashboard.addEventListener('click', e=>{
    li_d.classList.add("active")
    li_a.classList.remove("active")
    li_c.classList.remove("active")
})

about.addEventListener('click', e=>{
    li_d.classList.remove("active")
    li_a.classList.add("active")
    li_c.classList.remove("active")
})

contact.addEventListener('click', e=>{
    li_d.classList.remove("active")
    li_a.classList.remove("active")
    li_c.classList.add("active")
})