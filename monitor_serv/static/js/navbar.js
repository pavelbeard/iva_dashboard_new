const navLinkList = document.querySelectorAll('.nav-link');

for (let i = 0; i < navLinkList.length; i++) {
    const href = navLinkList[i].getAttribute('href');
    if (href.includes(document.URL.split('/').slice(-2,-1))) {
        navLinkList[i].className = 'nav-link active';
        break;
    }
}