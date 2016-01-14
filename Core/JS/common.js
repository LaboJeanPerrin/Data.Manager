// --- VARIABLES -----------------------------------------------------------

// The GET input
var $_GET = {};
document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
    function decode(s) {
        return decodeURIComponent(s.split("+").join(" "));
    }
    $_GET[decode(arguments[1])] = decode(arguments[2]);
});

var LANG;

// --- FUNCTIONS -----------------------------------------------------------

function mlt(en, fr) {
    switch (LANG) {
        case 'en': return en; 
        case 'fr': return fr; 
    }
}

// =========================================================================
//      ON DOCUMENT READY
// =========================================================================

$(function() {

    // Define language
    LANG = $('meta[Language]').attr("Language");
    
});