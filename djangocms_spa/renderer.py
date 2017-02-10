# coding=utf-8

class BaseSPARenderer(object):
    """
    Some base data needs to be available for all plugins.
    """
    frontend_component_name = ''
    plugin_class = None
    
    def render(self, request, plugin, instance=None, position=0, include_admin_data=False):
        context = {
            'content' : {},
            'position': position,
            'type'    : self.frontend_component_name
        }
        
        if include_admin_data:
            # This is the structure of the template `cms/toolbar/plugin.html` that is used to register
            # the frontend editing.
            context['cms'] = [
                'cms-plugin-{}'.format(instance.id),
                {
                    'type'                     : 'plugin',
                    'page_language'            : instance.language,
                    'placeholder_id'           : instance.placeholder.id,
                    'plugin_name'              : str(instance._meta.verbose_name),
                    'plugin_type'              : self.plugin_class.__class__.__name__,
                    'plugin_id'                : instance.id,
                    'plugin_language'          : instance.language,
                    'plugin_parent'            : instance.parent.id if instance.parent else None,
                    'plugin_order'             : instance.position,
                    'plugin_restriction'       : self.plugin_class.get_child_classes(instance.placeholder,
                                                                                     instance.page) or [],
                    'plugin_parent_restriction': self.plugin_class.get_parent_classes(instance.placeholder,
                                                                                      instance.page) or [],
                    'onClose'                  : False,
                    'addPluginHelpTitle'       : 'Add plugin to {parent_plugin_name}'.format(
                        parent_plugin_name=instance.get_plugin_name()),
                    'urls'                     : instance.get_action_urls()
                }
            ]
        
        return context


class MixinPluginRenderer(BaseSPARenderer):
    from .cms_plugins import SPAPluginMixin
    """
      Renders the plugins which use the SPAPluginMixin
    """
    
    def __init__(self, plugin_class: SPAPluginMixin):
        super().__init__()
        self.plugin_class = plugin_class
    
    @property
    def frontend_component_name(self):
        return self.plugin_class.frontend_component_name
    
    def render(self, request, plugin, instance=None, position=0, include_admin_data=False):
        context = super().render(request, plugin, instance, position, include_admin_data)
        return plugin.render_spa(request, context, instance, position, include_admin_data)
