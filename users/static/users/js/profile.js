$(document).ready(function() {
    $('.subscribe_to_profile-button').click(function() {
        var button = $(this);
        var profileId = button.data('profile-id');

        var data = {
            csrfmiddlewaretoken: CSRF_TOKEN,
            user_id: user_id,
            profile_id: profileId
        };

        $.ajax({
            url: '/user/toggle_profile_subscription/',
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
