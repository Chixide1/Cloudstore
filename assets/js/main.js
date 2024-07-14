window.onload = () => {
    highlight_navlink();
    add_upload();
}

function highlight_navlink(){
    let links = document.querySelectorAll('.nav-link')
    
    links.forEach(link => link.addEventListener('click', event => {
        let links = document.querySelectorAll('.nav-link')
        links.forEach(link => link.classList.remove('active'))
        event.currentTarget.classList.add('active')
    }))
}

function add_upload(){
    document.getElementById('upload-btn').addEventListener('click', () => {
        document.getElementById('upload-hidden').click();
    })
}