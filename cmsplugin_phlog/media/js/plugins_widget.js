(function($) {
	var addPlugin = function(plugin) {
		var type = plugin.find("select[name=plugins]").val();
		
		if (type) {
			$.ajax({
				url: "add-plugin/",
				dataType: "html",
				type: "POST",
				data: {
					plugin_type: type,
					parent_id:  plugin.data('id')
				},
				success: function(data) {
					plugin.find('ul').append('<li id="plugin_' + data +'">' + 
						'<span class="drag"></span>' + 
						'<span class="text">' + type + '</span>' + 
						'<span class="delete"></span></li>');
					editPlugin(data);
				},
				error: function(xhr) {
					
					if (xhr.status < 500) {
						alert(xhr.responseText);
					} else {
						$('.nested-plugins-error').html(xhr.responseText);
					}
				}
			});
		}
	};
	
	var editPlugin = function(plugin_id) {
		window.open("edit-plugin/"+plugin_id+"/?_popup=1",
				"Edit plugin",
				"menubar=no,titlebar=no,toolbar=no,resizable=yes" + 
				",width=800,height=300,top=0,left=0,scrollbars=yes" + 
				",location=no");
	};
	
	window.dismissEditPluginPopup = function(w, plugin_id, icon, alt) {
		w.close();
	};
	
	var deletePlugin = function(plugin_id) {
		var answer = confirm("Are you sure you want to delete this plugin?", true);
		if(answer){
			$.ajax({
				url: "remove-plugin/",
				dataType: "html",
				type: "POST",
				data: { plugin_id: plugin_id },
				success: function(data) {
					$('#plugin_'+ plugin_id).remove();
				},
				error: function(xhr) {
					if (xhr.status < 500) {
						alert(xhr.responseText);
					} else {
						$('.nested-plugins-error').html(xhr.responseText);
					}
				}
			});
		}
	};
	
	var installClickHandlers = function() {
		$('.nested-plugins .addlink').unbind('click');
		$('.nested-plugins .addlink').click(function(e) {
			e.preventDefault();
			e.stopPropagation();
			return addPlugin($(this).closest('.nested-plugins'));
		});
		
		$('.nested-plugins ul li .text').unbind('click');
		$('.nested-plugins ul li .text').click(function(e) {
			e.preventDefault();
			e.stopPropagation();
			return editPlugin($(this).closest('li').attr('id').substring(7));
		});
		
		$('.nested-plugins ul li .delete').unbind('click');
		$('.nested-plugins ul li .delete').click(function(e) {
			e.preventDefault();
			e.stopPropagation();
			return deletePlugin($(this).closest('li').attr('id').substring(7));
		});
	};
	
	var makePluginsSortable = function() {
		// Drag'n'Drop sorting/moving
		$('div.nested-plugins ul.plugin-list').sortable({
			handle:'span.drag',
			axis:'y',
			opacity:0.9,
			zIndex:2000,
			dropOnEmpty:true,
			update:function(event, ui){
				var array = $(this).sortable('toArray');
				var d = "";
				for(var i=0;i<array.length;i++){
					d += array[i].split("plugin_")[1];
					if (i!=array.length-1){
						d += "_";
					}
				}
				if (!ui.sender && d) {
					// moved in placeholder
					$.ajax({
						url: "move-plugin/",
						dataType: "json",
						type: "POST",
						data: { ids:d },
						error: function(xhr) {
							if (xhr.status < 500 && xhr.status > 200) {
								alert(xhr.responseText);
							} else if (xhr.status > 200) {
								$('.nested-plugins-error').html(xhr.responseText);
							}
						}
					});
				}
			}
		});
	};
	
	$(document).ready(function() {
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				function getCookie(name) {
					var cookieValue = null;
					if (document.cookie && document.cookie != '') {
						var cookies = document.cookie.split(';');
						for (var i = 0; i < cookies.length; i++) {
							var cookie = $.trim(cookies[i]);
							//Does this cookie string begin with the name we want?
							if (cookie.substring(0, name.length + 1) == (name + '=')) {
								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
								break;
							}
						}
					}
					return cookieValue;
				}
				var base_doc_url = document.URL.match(/^http[s]{0,1}:\/\/[^\/]+\//)[0];
				var base_settings_url = settings.url.match(/^http[s]{0,1}:\/\/[^\/]+\//);
				if (base_settings_url != null) {
					base_settings_url = base_settings_url[0];
				}
				if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)) || base_doc_url == base_settings_url) {
					// Only send the token to relative URLs i.e. locally.
					xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
				}
			}
		});
		
		installClickHandlers();
		makePluginsSortable();
		
	});
})(jQuery);