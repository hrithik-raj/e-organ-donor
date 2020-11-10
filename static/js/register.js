const username_field = document.querySelector('#username-field')
const email_field = document.querySelector('#email-field')
const register_button = document.querySelector('#submit_btn')
const password_field = document.querySelector('#password-field')
const mobile_field = document.querySelector('#mobile-number-field')

username_field.addEventListener('keyup', (e) => {
    e.preventDefault()
    const username_value = e.target.value
    if (username_value.length > 0) {
        fetch('/authentication/username_validation', {
            body: JSON.stringify(username_value),
            method: 'POST'
        }).then(
            res => res.json()
        ).then(
            data => {
                if (data['username_valid']) {
                    console.log(`username ${username_value} valid`)
                    username_field.classList.remove('is-invalid')
                    username_field.classList.add('is-valid')
                    register_button.removeAttribute('disabled')
                } else if (data['username_already_exists']) {
                    console.log(`username ${username_value} is already taken`)
                    username_field.classList.remove('is-valid')
                    username_field.classList.add('is-invalid')
                    register_button.setAttribute('disabled', 'disabled')
                }
            }
        )
    } else {
        username_field.classList.remove('is-valid')
        username_field.classList.remove('is-invalid')
        register_button.removeAttribute('disabled')
    }
})

email_field.addEventListener('keyup', (e) => {
    e.preventDefault()
    const email_value = e.target.value
    if (email_value.length > 0) {
        fetch('/authentication/email_validation', {
            body: JSON.stringify(email_value),
            method: 'POST'
        }).then(
            res => res.json()
        ).then(
            data => {
                if (data['email_valid']) {
                    console.log(`username ${email_value} valid`)
                    email_field.classList.remove('is-invalid')
                    email_field.classList.add('is-valid')
                    register_button.removeAttribute('disabled')
                } else {
                    console.log(`${data}`)
                    email_field.classList.remove('is-valid')
                    email_field.classList.add('is-invalid')
                    register_button.setAttribute('disabled', 'disabled')
                }
            }
        )
    } else {
        email_field.classList.remove('is-valid')
        email_field.classList.remove('is-invalid')
        register_button.removeAttribute('disabled')
    }
})

password_field.addEventListener('keyup', (e)=>{
    const password = e.target.value

    if (password.length < 4){
        password_field.classList.add('is-invalid')
        password_field.classList.remove('is-valid')
        register_button.setAttribute('disabled', 'disabled')
    }else{
        password_field.classList.add('is-valid')
        password_field.classList.remove('is-invalid')
        register_button.removeAttribute('disabled')
    }
     if (password.length === 0){
        password_field.classList.remove('is-valid')
        password_field.classList.remove('is-invalid')
        register_button.removeAttribute('disabled')
    }
})

mobile_field.addEventListener('keyup', (e)=>{
    const mobile = e.target.value

    if (mobile.length < 10 || mobile.length > 10){
        mobile_field.classList.add('is-invalid')
        mobile_field.classList.remove('is-valid')
        register_button.setAttribute('disabled', 'disabled')
    }else{
        mobile_field.classList.add('is-valid')
        mobile_field.classList.remove('is-invalid')
        register_button.removeAttribute('disabled')
    }
     if (mobile.length === 0){
        mobile_field.classList.remove('is-valid')
        mobile_field.classList.remove('is-invalid')
        register_button.removeAttribute('disabled')
    }
})
