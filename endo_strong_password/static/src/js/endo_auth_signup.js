openerp.endo_strong_password = function(instance){
    var module = instance.auth_signup // loading the namespace of the 'auth_signup' module

    instance.web.Login.include({
    
        get_params: function(){
            // signup user (or reset password)
            var db = this.$("form [name=db]").val();
            var name = this.$("form input[name=name]").val();
            var login = this.$("form input[name=login]").val();
            var password = this.$("form input[name=password]").val();
            var confirm_password = this.$("form input[name=confirm_password]").val();
            var strongRegex = new RegExp("^(?=.{6,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g"); 
            if (!db) {
                this.do_warn(_t("Login"), _t("No database selected !"));
                return false;
            } else if (!name) {
                this.do_warn(_t("Login"), _t("Please enter a name."));
                return false;
            } else if (!login) {
                this.do_warn(_t("Login"), _t("Please enter a username."));
                return false;
            } else if (!password || !confirm_password) {
                this.do_warn(_t("Login"), _t("Please enter a password and confirm it."));
                return false;
            } else if (password !== confirm_password) {
                this.do_warn(_t("Login"), _t("Passwords do not match; please retype them."));
                return false;
                
            }else if (!strongRegex.test(password)) {
                this.do_warn(_t("Login"), _t("Please use a password with at least 6 characters containing at least one numeric digit, one UPPERCASE, one lowercase letter and one Symbol character."));
                return false;
            }
            
            
            var params = {
                dbname : db,
                token: this.params.token || "",
                name: name,
                login: login,
                password: password,
            };
            return params;
        },
    });
};
