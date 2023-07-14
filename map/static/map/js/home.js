window.addEventListener('resize', updateHeight);
updateHeight();

function updateHeight() {
    var box = document.querySelector('.main-info_box');
    var boxContent = document.querySelector('.main-info_box-content');

    var originalDisplay = box.style.display;
    box.style.display = 'block';

    if (boxContent.scrollHeight > window.innerHeight) {
        box.style.height = '100%';
        boxContent.style.height = '100%';
    } else {
        box.style.height = '';
        boxContent.style.height = '';
    }

    box.style.display = originalDisplay;
}
