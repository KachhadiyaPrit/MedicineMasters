jQuery('#login_form').validate({
    rules:{
        email:{
            required:true,
            email:true
        },
        password:{
            required:true,
            minlength:8,
        }
    },
    messages:{
        email:{
            required:"Please enter your email...",
            email:"Please enter valid email...",
        },
        password:{
            required:"Please enter your password...",
            minlength:"Password must be 8 char long",
        }
    },
    submitHandler:function(form){
        form.submit();
    }
});

jQuery('#signup_form').validate({
    rules:{
        username:"required",
        email:{
            required:true,
            email:true
        },
        password:{
            required:true,
            minlength:8,
        },
        cpassword:{
            required:true,
            minlength:8,
            equalTo:"#cpassword"
        }
    },
    messages:{
        username:"Please enter your username...",
        email:{
            required:"Please enter your email...",
            email:"Please enter valid email...",
        },
        password:{
            required:"Please enter your password...",
            minlength:"Password must be 8 char long",
        },
        cpassword:{
            required:"Please enter your password...",
            minlength:"Password must be 8 char long",
            equalTo: "Please enter the same password as above"
        }
    },
    submitHandler:function(form){
        form.submit();
    }
});