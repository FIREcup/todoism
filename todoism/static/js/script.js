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

    function activeM() {
        $('.sidenav').sidenav();
        $('ul.tabs').tabs();
        $('.modal').modal();
        $('.tooltipped').tooltip();
        $('.dropdown-trigger').dropdown({
            constrainWidth: false,
            coverTrigger: false
        });
        display_dashboard();
    }

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

    function new_item(e) {
        var $input = $('#item-input');
        var value = $input.val().trim();
        if (e.which !== ENTER_KEY || !value) {
            return;
        }
        $input.focus().val('');
        $.ajax({
            type: 'POST',
            url: new_item_user,
            data: JSON.stringify({'body': value}),
            contentType: 'application/json,charset=UTF-8',
            success: function (data) {
                M.toast({html: data.message, classes: 'rounded'});
                $('.items').append(data.html);
                activeM();
                refresh_count();
            }
        });
    }

    $(document).on('keyup', '#item-input', new_item.bind(this));
});
