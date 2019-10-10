$(document).ready(
    function() {
        var ENTER_KEY = 13;
        var ESC_KEY = 27;

        $(document).ajaxError(function (event, request) {
            var message = null;

            if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
                message = request.responseJSON.message;
            } else if (request.responseText) {
                var IS_JSON = true;
                try {
                    var data = JSON.parse(request.responseText);
                }
                catch (err) {
                    IS_JSON = false;
                }

                if (IS_JSON && data != undefined && data.hasOwnProperty('message')) {
                    message = JSON.parse(request.responseText).message;
                } else {
                    message = default_error_message;
                }
            } else {
                message = default_error_message;
            }
            M.toast({html: message});
        });

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });

    $(window).bind('hashchange', function() {
        var hash = window.location.hash.replace('#', '');
        var url = null;
        if (hash == 'login') {
            url = login_page_url
        } else if (hash == 'app') {
            url = app_page_url
        } else {
            url = intro_page_url
        }

        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                $('#main').hide().html(data).fadeIn(800);
                activeM();
            }
        });
    });

    if (window.location.hash === '') {
        window.location.hash = '#intro';
    } else {
        $(window).trigger('hashchange');
    }

    function register() {
        $.ajax({
            type: 'GET',
            url: register_url,
            success: function (data) {
                $('#username-input').val(data.username);
                $('#password-input').val(data.password);
                M.toast({html: data.message})
            }
        });
    }

    $(document).on('click', '#register-btn', register);
});
