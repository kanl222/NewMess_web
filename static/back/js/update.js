$(document).ready(function() {
        $.ajax({
            type: "Get",
            url: "/api/jobs",
            dataType: "json",
            type: 'Get',
            cache: false,
            success: function(data) {
                console.log(data['jobs'][0])
                setTimeout(function() {show();}, 5000);
                localStorage['myKey'] = 'somestring';
            }
        });
    }
)
