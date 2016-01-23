var Esrc = new EventSource('Core/ServerEvents/location_update.py');

// -------------------------------------------------------------------------
function CloseEventSource() {
    $('#stop_update').hide();
    Esrc.close();
    console.log('Close server event');
    
    $('#cont_update').hide();
    $('#current_folder').html('');
    $('#update_folders').html('0');
    $('#update_files').html('0');
    $('#update_size').html('0 B');
}

// =========================================================================
//      ON DOCUMENT READY
// =========================================================================

$(function() {

    $('#update').click(function() {
        
        // --- Get parameters
        var IP = $("input[name='IP']").attr('value');
        var path = $("input[name='path']").attr('value');
        var jpath = $('#jpath').html();
        
        // --- Add stop button
        $('#stop_update').show();
        $('#cont_update').show();
        
        // --- Update
        console.log('Open server event');
        Esrc = new EventSource("Core/ServerEvents/location_update.py?ip="+IP+"&path="+path+"&jpath="+jpath);
        var nF = 0;
        
        Esrc.onmessage = function(e) {
            
            // --- Closing event
            if (e.data=='!CLOSE') { CloseEventSource() } 
            else {
                
                var tmp = e.data.split(': ');
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