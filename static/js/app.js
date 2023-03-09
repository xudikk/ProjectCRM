function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



$("document").ready(function(){
    $.fn.datepicker.defaults.format = "yyyy-mm-dd";
    $.fn.datepicker.defaults.autoclose = true;

    $('.timepick').datetimepicker({
        format: 'HH:mm', pickDate:false, autoclose: true,
    });


// $('#id_start_date').datepicker({});
//        $.ajaxSetup({
//            beforeSend: function (xhr, settings) {
//                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                }
//            }
//        });


        $('select[name="region"]').change(function(){

            if ($(this).val() != ""){

                objid = $(this).val()
                $('#id_district').empty();

                $.ajax({
                    url: '/api/v1/geo/district/'+objid+'/list/',
                    type: 'GET',
                    success: function (data) {
                        if (data){
                            $('#id_district').append('<option value=\"\"></option>');
                            $.each(data.items, function(id, item){
                                $('#id_district').append('<option value=\"'+item.id+'\">'+item.name+'</option>');
                            });
                        }
                    }

                });
            }
        });

        if ($('#id_period').length){


           $('select[name="group"]').change(function(){
           $('#id_period').empty();
            if ($(this).val() != ""){

                objid = $(this).val()
                $('#id_period').empty();

                $.ajax({
                    url: '/api/v1/education/period/'+objid+'/list/',
                    type: 'GET',
                    success: function (data) {
                        if (data){
                            $('#id_period').append('<option value=\"\"></option>');
                            $.each(data.items, function(id, item){
                                $('#id_period').append('<option value=\"'+item.id+'\">'+item.name+'</option>');
                            });
                        }
                    }

                });
            }
        });


        }



    });