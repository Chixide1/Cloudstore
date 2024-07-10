window.onload = () => {
    let links = document.querySelectorAll('.nav-link')
    
    links.forEach(link => link.addEventListener('click', event => {
        let links = document.querySelectorAll('.nav-link')
        links.forEach(link => link.classList.remove('active'))
        event.currentTarget.classList.add('active')
    }))
}
