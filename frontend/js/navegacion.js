
function navigate(page) {
    window.location.href = page + '.html';
}

function logout() {
    localStorage.removeItem('usuario');
    sessionStorage.clear();
    
    window.location.href = 'login.html';
}


document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop().replace('.html', '');
    
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.classList.remove('active');
        
        const onclickAttr = item.getAttribute('onclick');
        
        if (onclickAttr) {
            const match = onclickAttr.match(/navigate\(['"](.+)['"]\)/);
            if (match && match[1] === currentPage) {
                item.classList.add('active');
            }
        }
    });
});