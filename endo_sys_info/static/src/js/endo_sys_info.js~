openerp.endo_sys_info = function(instance){
	var _t = instance.web._t,
    _lt = instance.web._lt;
	var QWeb = instance.web.qweb;
	instance.web.form.widgets.add('twotomany', 'instance.web.form.TwotoMany');
var commands = {
    // (0, _, {values})
    CREATE: 0,
    'create': function (values) {
        return [commands.CREATE, false, values];
    },
    // (1, id, {values})
    UPDATE: 1,
    'update': function (id, values) {
        return [commands.UPDATE, id, values];
    },
    // (2, id[, _])
    DELETE: 2,
    'delete': function (id) {
        return [commands.DELETE, id, false];
    },
    // (3, id[, _]) removes relation, but not linked record itself
    FORGET: 3,
    'forget': function (id) {
        return [commands.FORGET, id, false];
    },
    // (4, id[, _])
    LINK_TO: 4,
    'link_to': function (id) {
        return [commands.LINK_TO, id, false];
    },
    // (5[, _[, _]])
    DELETE_ALL: 5,
    'delete_all': function () {
        return [5, false, false];
    },
    // (6, _, ids) replaces all linked records with provided ids
    REPLACE_WITH: 6,
    'replace_with': function (ids) {
        return [6, false, ids];
    }
};	
	
instance.web.form.TwotoMany = instance.web.form.AbstractField.extend({

	multi_selection: false,
    disable_utility_classes: true,
    init: function(field_manager, node) {
        this._super(field_manager, node);
        this.is_loaded = $.Deferred();
        this.initial_is_loaded = this.is_loaded;
        this.form_last_update = $.Deferred();
        this.init_form_last_update = this.form_last_update;
        this.is_started = false;
        this.dataset = new instance.web.form.One2ManyDataSet(this, this.field.relation);
        this.dataset.o2m = this;
        this.dataset.parent_view = this.view;
        this.dataset.child_name = this.name;
        this.part_line = new instance.web.Model('room.lines');
        this.part_item = new instance.web.Model('licensce.lines');
        var self = this;
        this.dataset.on('dataset_changed', this, function() {
            self.trigger_on_change();
        });
        this.set_value([]);
    },
    start: function() {
        this._super.apply(this, arguments);
        this.$el.addClass('oe_form_field oe_form_field_one2many');

        var self = this;

        self.load_views();
        this.is_loaded.done(function() {
            self.on("change:effective_readonly", self, function() {
                self.is_loaded = self.is_loaded.then(function() {
                    self.viewmanager.destroy();
                    return $.when(self.load_views()).done(function() {
                        self.reload_current_view();
                    });
                });
            });
        });
        this.is_started = true;
        this.reload_current_view();
    },
	
	
     trigger_on_change: function() {
        this.trigger('changed_value');
    },
    load_views: function() {
        var self = this;
        var modes = this.node.attrs.mode;
        modes = !!modes ? modes.split(",") : ["tree"];
        var views = [];
        _.each(modes, function(mode) {
            if (! _.include(["list", "tree", "graph", "kanban"], mode)) {
                throw new Error(_.str.sprintf(_t("View type '%s' is not supported in One2Many."), mode));
            }
            var view = {
                view_id: false,
                view_type: mode == "tree" ? "list" : mode,
                options: {}
            };
            
            if (self.field.views && self.field.views[mode]) {
                view.embedded_view = self.field.views[mode];
            }
            
            if(view.view_type === "list") {
                _.extend(view.options, {
                    addable: null,
                    selectable: self.multi_selection,
                    sortable: false,
                    import_enabled: false,
                    deletable: true
                });
                if (self.get("effective_readonly")) {
                    _.extend(view.options, {
                        deletable: null,
                        reorderable: false,
                    });
                }
            } else if (view.view_type === "form") {
                if (self.get("effective_readonly")) {
                    view.view_type = 'form';
                }
                _.extend(view.options, {
                    not_interactible_on_create: true,
                });
            } else if (view.view_type === "kanban") {
                _.extend(view.options, {
                    confirm_on_delete: false,
                });
                if (self.get("effective_readonly")) {
                    _.extend(view.options, {
                        action_buttons: false,
                        quick_creatable: false,
                        creatable: false,
                        read_only_mode: true,
                    });
                }
            } 
            views.push(view);
        });
        this.views = views;
        this.viewmanager = new instance.web.form.One2ManyENDOViewManager(this, this.dataset, views, {});
        this.viewmanager.o2m = self;
        var once = $.Deferred().done(function() {
            self.init_form_last_update.resolve();
        });
        var def = $.Deferred().done(function() {
            self.initial_is_loaded.resolve();

        });
        this.viewmanager.on("controller_inited", self, function(view_type, controller) {
            controller.o2m = self;
            if (view_type == "list") {
                if (self.get("effective_readonly")) {
                    controller.on('edit:before', self, function (e) {
                        e.cancel = true;
                    });
                    _(controller.columns).find(function (column) {
                        if (!(column instanceof instance.web.list.Handle)) {
                            return false;
                        }
                        column.modifiers.invisible = true;
                        return true;
                    });
                }
            } else if (view_type === "form") {
                if (self.get("effective_readonly")) {
                    $(".oe_form_buttons", controller.$el).children().remove();
                }
                controller.on("load_record", self, function(){
                     once.resolve();
                 });
                controller.on('pager_action_executed',self,self.save_any_view);
            } else if (view_type == "graph") {
                self.reload_current_view()
            }
            def.resolve();
        });
        this.viewmanager.on("switch_mode", self, function(n_mode, b, c, d, e) {
            $.when(self.save_any_view()).done(function() {
                if (n_mode === "list") {
                    $.async_when().done(function() {
                        self.reload_current_view();
                    });
                }
            });
        });
        $.async_when().done(function () {
            self.viewmanager.appendTo(self.$el);
        });
        return def;
    },
    reload_current_view: function() {
        var self = this;
        return self.is_loaded = self.is_loaded.then(function() {
            var active_view = self.viewmanager.active_view;
            var view = self.viewmanager.views[active_view].controller;
            if(active_view === "list") {
                return view.reload_content();
            } else if (active_view === "form") {
                if (self.dataset.index === null && self.dataset.ids.length >= 1) {
                    self.dataset.index = 0;
                }
                var act = function() {
                    return view.do_show();
                };
                self.form_last_update = self.form_last_update.then(act, act);
                return self.form_last_update;
            } else if (view.do_search) {
                return view.do_search(self.build_domain(), self.dataset.get_context(), []);
            }
        }, undefined);
    },
    set_value: function(value_) {
        value_ = value_ || [];
        var self = this;
        this.dataset.reset_ids([]);
        if(value_.length >= 1 && value_[0] instanceof Array) {
            var ids = [];
            _.each(value_, function(command) {
                var obj = {values: command[2]};
                switch (command[0]) {
                    case commands.CREATE:
                        obj['id'] = _.uniqueId(self.dataset.virtual_id_prefix);
                        obj.defaults = {};
                        self.dataset.to_create.push(obj);
                        self.dataset.cache.push(_.extend(_.clone(obj), {values: _.clone(command[2])}));
                        ids.push(obj.id);
                        return;
                    case commands.UPDATE:
                        obj['id'] = command[1];
                        self.dataset.to_write.push(obj);
                        self.dataset.cache.push(_.extend(_.clone(obj), {values: _.clone(command[2])}));
                        ids.push(obj.id);
                        return;
                    case commands.DELETE:
                        self.dataset.to_delete.push({id: command[1]});
                        return;
                    case commands.LINK_TO:
                        ids.push(command[1]);
                        return;
                    case commands.DELETE_ALL:
                        self.dataset.delete_all = true;
                        return;
                }
            });
            this._super(ids);
            this.dataset.set_ids(ids);
        } else if (value_.length >= 1 && typeof(value_[0]) === "object") {
            var ids = [];
            this.dataset.delete_all = true;
            _.each(value_, function(command) {
                var obj = {values: command};
                obj['id'] = _.uniqueId(self.dataset.virtual_id_prefix);
                obj.defaults = {};
                self.dataset.to_create.push(obj);
                self.dataset.cache.push(_.clone(obj));
                ids.push(obj.id);
            });
            this._super(ids);
            this.dataset.set_ids(ids);
        } else {
            this._super(value_);
            this.dataset.reset_ids(value_);
        }
        if (this.dataset.index === null && this.dataset.ids.length > 0) {
            this.dataset.index = 0;
        }
        this.trigger_on_change();
        if (this.is_started) {
            return self.reload_current_view();
        } else {
            return $.when();
        }
    },
    get_value: function() {
        var self = this;
        if (!this.dataset)
            return [];
        var val = this.dataset.delete_all ? [commands.delete_all()] : [];
        val = val.concat(_.map(this.dataset.ids, function(id) {
        	
            var alter_order = _.detect(self.dataset.to_create, function(x) {return x.id === id;});
            if (alter_order) {
                return commands.create(alter_order.values);
            }
            alter_order = _.detect(self.dataset.to_write, function(x) {return x.id === id;});
            if (alter_order) {
                return commands.update(alter_order.id, alter_order.values);
            }
            return commands.link_to(id);
        }));
        return val.concat(_.map(
            this.dataset.to_delete, function(x) {
                return commands['delete'](x.id);}));
    },
    commit_value: function() {
        return this.save_any_view();
    },
    save_any_view: function() {
        if (this.viewmanager && this.viewmanager.views && this.viewmanager.active_view &&
            this.viewmanager.views[this.viewmanager.active_view] &&
            this.viewmanager.views[this.viewmanager.active_view].controller) {
            var view = this.viewmanager.views[this.viewmanager.active_view].controller;
            if (this.viewmanager.active_view === "form") {
                if (!view.is_initialized.state() === 'resolved') {
                    return $.when(false);
                }
                return $.when(view.save());
            } else if (this.viewmanager.active_view === "list") {
                return $.when(view.ensure_saved());
            }
        }
        return $.when(false);
    },
    is_syntax_valid: function() {
        if (! this.viewmanager || ! this.viewmanager.views[this.viewmanager.active_view])
            return true;
        var view = this.viewmanager.views[this.viewmanager.active_view].controller;
        switch (this.viewmanager.active_view) {
        case 'form':
            return _(view.fields).chain()
                .invoke('is_valid')
                .all(_.identity)
                .value();
            break;
        case 'list':
            return view.is_valid();
        }
        return true;
    },
    
    
	});

instance.web.form.One2ManyENDOViewManager = instance.web.ViewManager.extend({
    template: 'One2ManyENDO.viewmanager',
    init: function(parent, dataset, views, flags) {
        this._super(parent, dataset, views, _.extend({}, flags, {$sidebar: false}));
        this.registry = this.registry.extend({
            list: 'instance.web.form.One2ManyENDOListView',
            form: 'instance.web.form.One2ManyENDOFormView',
        });
        this.__ignore_blur = false;
    },
    switch_mode: function(mode, unused) {
        if (mode !== 'form') {
            return this._super(mode, unused);
        }
        var self = this;
        var id = self.o2m.dataset.index !== null ? self.o2m.dataset.ids[self.o2m.dataset.index] : null;
        var pop = new instance.web.form.FormOpenPopup(this);
        pop.show_element(self.o2m.field.relation, id, self.o2m.build_context(), {
            title: _t("Open: ") + self.o2m.string,
            create_function: function(data, options) {
                return self.o2m.dataset.create(data, options).done(function(r) {
                    self.o2m.dataset.set_ids(self.o2m.dataset.ids.concat([r]));
                    self.o2m.dataset.trigger("dataset_changed", r);
                });
            },
            write_function: function(id, data, options) {
                return self.o2m.dataset.write(id, data, {}).done(function() {
                    self.o2m.reload_current_view();
                });
            },
            alternative_form_view: self.o2m.field.views ? self.o2m.field.views["form"] : undefined,
            parent_view: self.o2m.view,
            child_name: self.o2m.name,
            read_function: function() {
                return self.o2m.dataset.read_ids.apply(self.o2m.dataset, arguments);
            },
            form_view_options: {'not_interactible_on_create':true},
            readonly: self.o2m.get("effective_readonly")
        });
        pop.on("elements_selected", self, function() {
            self.o2m.reload_current_view();
        });
    },
});

instance.web.form.One2ManyENDODataSet = instance.web.BufferedDataSet.extend({
    get_context: function() {
        this.context = this.o2m.build_context();
        return this.context;
    }
});

instance.web.form.One2ManyENDOListView = instance.web.ListView.extend({
    _template: 'One2ManyENDO.listview',
    init: function (parent, dataset, view_id, options) {
        this._super(parent, dataset, view_id, _.extend(options || {}, {
            GroupsType: instance.web.form.One2ManyENDOGroups,
            ListType: instance.web.form.One2ManyENDOList
        }));
        this.on('edit:before', this, this.proxy('_before_edit'));
        this.on('edit:after', this, this.proxy('_after_edit'));
        this.on('save:before cancel:before', this, this.proxy('_before_unedit'));

        this.records
            .bind('add', this.proxy("changed_records"))
            .bind('edit', this.proxy("changed_records"))
            .bind('remove', this.proxy("changed_records"));
    },
    start: function () {
        var ret = this._super();
        this.$el
            .off('mousedown.handleButtons')
            .on('mousedown.handleButtons', 'table button', this.proxy('_button_down'));
        
        return ret;
    },
    changed_records: function () {
        this.o2m.trigger_on_change();
    },
    is_valid: function () {
        var editor = this.editor;
        var form = editor.form;
        // If no edition is pending, the listview can not be invalid (?)
        if (!editor.record) {
            return true
        }
        // If the form has not been modified, the view can only be valid
        // NB: is_dirty will also be set on defaults/onchanges/whatever?
        // oe_form_dirty seems to only be set on actual user actions
        if (!form.$el.is('.oe_form_dirty')) {
            return true;
        }
        this.o2m._dirty_flag = true;

        // Otherwise validate internal form
        return _(form.fields).chain()
            .invoke(function () {
                this._check_css_flags();
                return this.is_valid();
            })
            .all(_.identity)
            .value();
    },
    do_add_record: function () {
        if (this.editable()) {
            this._super.apply(this, arguments);
        } else {
            var self = this;
            var pop = new instance.web.form.SelectCreatePopup(this);
            pop.select_element(
                self.o2m.field.relation,
                {
                    title: _t("Create: ") + self.o2m.string,
                    initial_view: "form",
                    alternative_form_view: self.o2m.field.views ? self.o2m.field.views["form"] : undefined,
                    create_function: function(data, options) {
                        return self.o2m.dataset.create(data, options).done(function(r) {
                            self.o2m.dataset.set_ids(self.o2m.dataset.ids.concat([r]));
                            self.o2m.dataset.trigger("dataset_changed", r);
                            self.dsa_add_new(r,data);
                            
                        });
                    },
                    read_function: function() {
                        return self.o2m.dataset.read_ids.apply(self.o2m.dataset, arguments);
                    },
                    parent_view: self.o2m.view,
                    child_name: self.o2m.name,
                    form_view_options: {'not_interactible_on_create':true}
                },
                self.o2m.build_domain(),
                self.o2m.build_context()
            );
            pop.on("elements_selected", self, function() {
                self.o2m.reload_current_view();
            });
        }
    },
    
    dsa_add_new:function(id, data){
    	var self =this;
    	$.each(this.dataset.cache, function(key,value){
    		if(value.values.hasOwnProperty("sub_item")){
    			setTimeout(function(){
    			var myview = self.$el.find('tr[data-id='+ value.id +']');
    			$.each(value.values.sub_item,function(inner_key,iner_value){
    			if(iner_value[0] == 0) {   //add item 
					myview.after("<tr class='oe_group_header' name='"+ value.id +"' style='background:#fff'><td class='oe_list_group_name'><span style='float: left; white-space: pre;'></span><span class='ui-icon' style='float: left; background-position: 150px 150px'></span>" +
					iner_value[2].name+ "</td><td class='oe_number'>"+ 
					iner_value[2].comp_name +"</td><td class='oe_number'>"+
					iner_value[2].installed_date+"</td><td class='oe_number'>"+
					iner_value[2].support_start+"</td><td class='oe_number'>"+
					iner_value[2].support_end+"</td></tr>");
	    		}
    	});
    		},1000);}});
    },
    dsa_change_viewlist:function(id,data){
    	var self = this;
    	$.each(this.dataset.cache, function(key,value){
    		if(value.values.hasOwnProperty("sub_item")){
    			var myview = self.$el.find('tr[data-id='+ value.id +']');
    			$.each(value.values.sub_item,function(inner_key,iner_value){
    			if(iner_value[0] == 0) {   //add item 
					myview.after("<tr class='oe_group_header' name='"+ value.id +"' style='background:#fff'><td class='oe_list_group_name'><span style='float: left; white-space: pre;'></span><span class='ui-icon' style='float: left; background-position: 150px 150px'></span>" +
					iner_value[2].name+ "</td><td class='oe_number'>"+ 
					iner_value[2].comp_name +"</td><td class='oe_text_center'>"+
					iner_value[2].installed_date+"</td><td class='oe_text_center'>"+
					iner_value[2].support_start+"</td><td class='oe_number'>"+
					iner_value[2].support_end+"</td></tr>");
	    		}
    			else if(iner_value[0] == 2){  //delete item   delay 1 sec exec, not the best method
    				setTimeout(function(){self.$el.find('tr[id="'+iner_value[1] +'"]').hide();}, 1000);
    			}
    			else if(iner_value[0] == 1){  //change item
    				setTimeout(function(){
    					self.$el.find('tr[id="'+iner_value[1] +'"]').hide();
    					myview.after("<tr class='oe_group_header' name='"+ value.id +"' style='background:#fff'><td class='oe_list_group_name'><span style='float: left; white-space: pre;'></span><span class='ui-icon' style='float: left; background-position: 150px 150px'></span>" +
						iner_value[2].name+ "</td><td class='oe_number'>"+ 
						iner_value[2].comp_name +"</td><td class='oe_text_center'>"+
						iner_value[2].installed_date+"</td><td class='oe_text_center'>"+
						iner_value[2].support_start+"</td><td class='oe_number'>"+
					    iner_value[2].support_end+"</td></tr>");
    				}, 1000);
    			}
    		});
    		}
    	});
    },
    
    
    do_activate_record: function(index, id) {
        var self = this;
        var pop = new instance.web.form.FormOpenPopup(self);
        pop.show_element(self.o2m.field.relation, id, self.o2m.build_context(), {
            title: _t("Open: ") + self.o2m.string,
            write_function: function(id, data) {
                return self.o2m.dataset.write(id, data, {}).done(function() {
                    self.o2m.reload_current_view().done(function(){
                    	self.dsa_change_viewlist(id,data);
                    });
                });
            },
            alternative_form_view: self.o2m.field.views ? self.o2m.field.views["form"] : undefined,
            parent_view: self.o2m.view,
            child_name: self.o2m.name,
            read_function: function() {
                return self.o2m.dataset.read_ids.apply(self.o2m.dataset, arguments);
            },
            form_view_options: {'not_interactible_on_create':true},
            readonly: !this.is_action_enabled('edit') || self.o2m.get("effective_readonly")
        });
    },
    do_button_action: function (name, id, callback) {
        if (!_.isNumber(id)) {
            instance.webclient.notification.warn(
                _t("Action Button"),
                _t("The o2m record must be saved before an action can be used"));
            return;
        }
        var parent_form = this.o2m.view;
        var self = this;
        this.ensure_saved().then(function () {
            if (parent_form)
                return parent_form.save();
            else
                return $.when();
        }).done(function () {
            self.handle_button(name, id, callback);
        });
    },

    _before_edit: function () {
        this.__ignore_blur = false;
        this.editor.form.on('blurred', this, this._on_form_blur);
    },
    _after_edit: function () {
        // The form's blur thing may be jiggered during the edition setup,
        // potentially leading to the o2m instasaving the row. Cancel any
        // blurring triggered the edition startup here
        this.editor.form.widgetFocused();
    },
    _before_unedit: function () {
        this.editor.form.off('blurred', this, this._on_form_blur);
    },
    _button_down: function () {
        // If a button is clicked (usually some sort of action button), it's
        // the button's responsibility to ensure the editable list is in the
        // correct state -> ignore form blurring
        this.__ignore_blur = true;
    },
    /**
     * Handles blurring of the nested form (saves the currently edited row),
     * unless the flag to ignore the event is set to ``true``
     *
     * Makes the internal form go away
     */
    _on_form_blur: function () {
        if (this.__ignore_blur) {
            this.__ignore_blur = false;
            return;
        }
        // FIXME: why isn't there an API for this?
        if (this.editor.form.$el.hasClass('oe_form_dirty')) {
            this.ensure_saved();
            return;
        }
        this.cancel_edition();
    },
    keyup_ENTER: function () {
        // blurring caused by hitting the [Return] key, should skip the
        // autosave-on-blur and let the handler for [Return] do its thing (save
        // the current row *anyway*, then create a new one/edit the next one)
        this.__ignore_blur = true;
        this._super.apply(this, arguments);
    },
    do_delete: function (ids) {
    	var self = this;
    	$.each(ids, function(key,value){
    		self.$el.find("tr[name='"+ value +"']").hide();
    	});
        var confirm = window.confirm;
        window.confirm = function () { return true; };
        try {
            return this._super(ids);
        } finally {
            window.confirm = confirm;
        }
    }
});
instance.web.form.One2ManyENDOGroups = instance.web.ListView.Groups.extend({
    setup_reseqlistviewuence_rows: function () {
        if (!this.view.o2m.get('effective_readonly')) {
            this._super.apply(this, arguments);
        }
    }
});
instance.web.form.One2ManyENDOList = instance.web.ListView.List.extend({
	 render_cell: function (record, column) {
        var value;
        if(column.type === 'reference') {
            value = record.get(column.id);
            var ref_match;
            // Ensure that value is in a reference "shape", otherwise we're
            // going to loop on performing name_get after we've resolved (and
            // set) a human-readable version. m2o does not have this issue
            // because the non-human-readable is just a number, where the
            // human-readable version is a pair
            if (value && (ref_match = /^([\w\.]+),(\d+)$/.exec(value))) {
                // reference values are in the shape "$model,$id" (as a
                // string), we need to split and name_get this pair in order
                // to get a correctly displayable value in the field
                var model = ref_match[1],
                    id = parseInt(ref_match[2], 10);
                new instance.web.DataSet(this.view, model).name_get([id]).done(function(names) {
                    if (!names.length) { return; }
                    record.set(column.id, names[0][1]);
                });
            }
        } else if (column.type === 'many2one') {
            value = record.get(column.id);
            // m2o values are usually name_get formatted, [Number, String]
            // pairs, but in some cases only the id is provided. In these
            // cases, we need to perform a name_get call to fetch the actual
            // displayable value
            if (typeof value === 'number' || value instanceof Number) {
                // fetch the name, set it on the record (in the right field)
                // and let the various registered events handle refreshing the
                // row
                new instance.web.DataSet(this.view, column.relation)
                        .name_get([value]).done(function (names) {
                    if (!names.length) { return; }
                    record.set(column.id, names[0]);
                });
            }
        } else if (column.type === 'many2many') {
            // non-resolved (string) m2m values are arrays
            if (value instanceof Array && !_.isEmpty(value)
                    && !record.get(column.id + '__display')) {
                var ids;
                // they come in two shapes:
                if (value[0] instanceof Array) {
                    var command = value[0];
                    // 1. an array of m2m commands (usually (6, false, ids))
                    if (command[0] !== 6) {
                        throw new Error(_.str.sprintf( _t("Unknown m2m command %s"), command[0]));
                    }
                    ids = command[2];
                } else {
                    // 2. an array of ids
                    ids = value;
                }
                new instance.web.Model(column.relation)
                    .call('name_get', [ids]).done(function (names) {
                        // FIXME: nth horrible hack in this poor listview
                        record.set(column.id + '__display',
                                   _(names).pluck(1).join(', '));
                        record.set(column.id, ids);
                    });
                // temp empty value
                record.set(column.id, false);
            }
        } 
        return column.format(record.toForm().data, {
            model: this.dataset.model,
            id: record.get('id')
        });
    },
	
	render: function () {
        this.$current.empty().append(
            QWeb.render('EndoListView.rows', _.extend({
                    render_cell: function () {
                        return self.render_cell.apply(self, arguments); }
                }, this)));
        this.pad_table_to(4);
    },
    dsa_list_view:function(){
   		var current = this.$current;
    	var ids = this.dataset.ids;
    	var lineModel = new instance.web.Model("licensce.lines")
    	for(i = 0; i < ids.length;i++){
    		if(isNaN(ids[i])) continue;
    		current.find('tr[data-id='+ ids[i] +']').css("background","#E4E5E4");
    		lineModel.query().filter([['licenscee_id','=',ids[i]]]).all().done(function(item){
    			if(item.length == 0) return;
    			var myview = current.find('tr[data-id='+ item[0].licenscee_id[0] +']');
           		$.each(item,function(key, value){
						myview.after("<tr class='oe_group_header'  id='" + value.id+ "' name='" + value.licenscee_id[0] + "' style='background:#fff'><td class='oe_list_group_name'><span style='float: left; white-space: pre;'></span><span class='ui-icon' style='float: left; background-position: 150px 150px'></span>" +
                        "</td><td class='oe_text_left'>"+ 
						 value.name[1]+ "</td><td class='oe_text_left'>"+ 
						 value.comp_name +"</td><td class='oe_text_left'>"+
						 value.installed_date +"</td><td class='oe_text_left'>"+
						 value.support_start +"</td><td class='oe_text_left'>"+
						 value.support_end +"</td></tr>");
					});
           });
    	}
    },
    
    pad_table_to: function (count) {
    	this.dsa_list_view();
        if (!this.view.is_action_enabled('create')) {
            this._super(count);
        } else {
            this._super(count > 0 ? count - 1 : 0);
        }

        // magical invocation of wtf does that do
        if (this.view.o2m.get('effective_readonly')) {
            return;
        }

        var self = this;
        var columns = _(this.columns).filter(function (column) {
            return column.invisible !== '1';
        }).length;
        if (this.options.selectable) { columns++; }
        if (this.options.deletable) { columns++; }

        if (!this.view.is_action_enabled('create')) {
            return;
        }

        var $cell = $('<td>', {
            colspan: columns + 3,
            'class': 'oe_form_field_one2many_list_row_add'
        }).append(
            $('<a>', {href: '#'}).text(_t("Add an item"))
                .mousedown(function () {
                    // FIXME: needs to be an official API somehow
                    if (self.view.editor.is_editing()) {
                        self.view.__ignore_blur = true;
                    }
                })
                .click(function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    // FIXME: there should also be an API for that one
                    if (self.view.editor.form.__blur_timeout) {
                        clearTimeout(self.view.editor.form.__blur_timeout);
                        self.view.editor.form.__blur_timeout = false;
                    }
                    self.view.ensure_saved().done(function () {
                        self.view.do_add_record();
                    });
                }));

        var $padding = this.$current.find('tr:not([data-id]):first');
        var $newrow = $('<tr>').append($cell);
        if ($padding.length) {
            $padding.before($newrow);
        } else {
            this.$current.append($newrow);
        }
    }
});

instance.web.form.One2ManyENDOFormView = instance.web.FormView.extend({
    form_template: 'One2ManyENDO.formview',
    load_form: function(data) {
        this._super(data);
        var self = this;
        this.$buttons.find('button.oe_form_button_create').click(function() {
            self.save().done(self.on_button_new);
        });
    },
    do_notify_change: function() {
        if (this.dataset.parent_view) {
            this.dataset.parent_view.do_notify_change();
        } else {
            this._super.apply(this, arguments);
        }
    }
});
	
	
	
instance.web.form.widgets = instance.web.form.widgets.extend({
    'twotomany' : 'instance.web.form.TwotoMany',
});
	
}


   
