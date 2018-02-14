//     var x = window.location.pathname;
//     console.log(x);
//     $('ul li a[href*="'+x+'"]').addClass('active');

var x = window.location.pathname;
console.log(x);
$('ul li a[href="' + x + '"]').closest('li').addClass('active');