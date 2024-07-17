window.onload = () => {
    highlight_navlink();
    add_upload();
}

function highlight_navlink(){
    let links = document.querySelectorAll('.sidebar__link')
    
    links.forEach(link => link.addEventListener('click', event => {
        links.forEach(link => link.classList.remove('sidebar__link--active'))
        event.currentTarget.classList.add('sidebar__link--active')
    }))
}

function add_upload(){
    document.querySelector('#upload-btn').addEventListener('click', () => {
        document.querySelector('#upload-hidden').click();
    })
}