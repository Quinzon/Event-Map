$(document).ready(function() {
    $('.subscribe-button').click(function() {
        var button = $(this);
        var eventInnerId = button.data('event-inner-id') || '';
        var eventApiId = button.data('event-api-id') || '';

        var data = {
            csrfmiddlewaretoken: CSRF_TOKEN,
            user_id: user_id,
            event_inner_id: eventInnerId,
            event_api_id: eventApiId
        };

        $.ajax({
            url: '/toggle_event_subscription/',
            method: 'POST',
            data: data,
            success: function(response) {
                if (response.subscribed) {
                    button.text('Отписаться');
                } else {
                    button.text('Подписаться');
                }
            }
        });
    });
});
