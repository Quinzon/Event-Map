$(document).ready(function() {
    $('.subscribe_to_profile').click(function() {
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
                    button.text('Вы подписаны');
                } else {
                    button.text('Подписаться');
                }
            }
        });
    });
});
$(document).ready(function() {
    $('.subscribe_to_event').click(function() {
        var button = $(this);
        var event_inner_id = button.data('event-id');
        var data = {
            csrfmiddlewaretoken: CSRF_TOKEN,
            user_id: user_id,
            event_inner_id: event_inner_id,
            event_api_id: '',
        };

        $.ajax({
            url: '/toggle_event_subscription/',
            method: 'POST',
            data: data,
            success: function(response) {
                if (response.subscribed) {
                    button.text('Вы подписаны');
                } else {
                    button.text('Подписаться');
                }
            }
        });
    });
});
$(document).ready(function() {
    var modal = document.querySelector(".main-modal_favorite_profiles");
    var btn = document.querySelector(".main-favorite_profiles");
    var span = document.getElementsByClassName("main-modal_favorite_profiles-close")[0];
    btn.onclick = function() {
      modal.style.display = "block";
    }
    span.onclick = function() {
      modal.style.display = "none";
    }
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
});