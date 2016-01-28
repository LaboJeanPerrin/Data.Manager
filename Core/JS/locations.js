var Esrc = new EventSource('Core/ServerEvents/location_update.py');

// -------------------------------------------------------------------------
function htmldecode(value){ return $('<div/>').html(value).text(); }

// -------------------------------------------------------------------------
function CloseEventSource() {
    $('#stop_update').hide();
    Esrc.close();
    
    // Reload (without POST)
    // window.location.href = window.location.href;
}

// --- View functions

function toggle_view(id) { $('#view_'+id).toggle(); }
function fold_all() { $("span[id^='view_']").hide(); }
function unfold_all() { $("span[id^='view_']").show(); }


// =========================================================================
//      ON DOCUMENT READY
// =========================================================================

$(function() {

    $('#update').click(function() {
        
        // --- Get parameters
        var IP = $("input[name='IP']").attr('value');
        var path = $("input[name='path']").attr('value');
        var name = $("input[name='name']").attr('value');
        var jpath = $('#jpath').html();
        
        // --- Add stop button
        $('#stop_update').show();
        $('#cont_update').show();
        
        // --- Update
        Esrc = new EventSource("Core/ServerEvents/location_update.py?ip="+IP+"&path="+path+"&name="+name+"&jpath="+jpath);
        var nF = 0;
        
        Esrc.onmessage = function(e) {
            
            console.log(htmldecode(e.data));
            
            // --- Closing event
            switch (htmldecode(e.data)) {
                
                case '!CLOSE':
                    CloseEventSource();
                    break;
                    
                case '!IMPORT':
                    // console.log('import');
                    break;
                    
                default:
                
                    var tmp = htmldecode(e.data).split(': ');
                    switch (tmp[0]) {
                        case 'folder':
                            nF++;
                            $('#current_folder').html(tmp[1]);
                            $('#update_folders').html(Number(nF).toLocaleString('en'));
                            break;
                        case 'stat':
                            tmp = tmp[1].split(' ');
                            $('#update_files').html(Number(tmp[0]).toLocaleString('en'));
                            $('#update_size').html(tmp[1]+' '+tmp[2]);
                            break;
                        case 'debug':
                            console.log(tmp[1]);
                            break;
                    }
            }
        }
        
    });
    
    $('#stop_update').click(function() { CloseEventSource() });
    
});