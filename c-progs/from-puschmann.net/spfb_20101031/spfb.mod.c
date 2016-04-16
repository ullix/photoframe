#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
 .name = KBUILD_MODNAME,
 .init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
 .exit = cleanup_module,
#endif
 .arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x8d396e8a, "module_layout" },
	{ 0xb0dff4f0, "sys_imageblit" },
	{ 0x8138235, "sys_copyarea" },
	{ 0x3a3064ee, "sys_fillrect" },
	{ 0xd34ab841, "fb_sys_read" },
	{ 0xa2c56c31, "param_ops_ulong" },
	{ 0x528c709d, "simple_read_from_buffer" },
	{ 0xb00ccc33, "finish_wait" },
	{ 0xe75663a, "prepare_to_wait" },
	{ 0x4292364c, "schedule" },
	{ 0xc8b57c27, "autoremove_wake_function" },
	{ 0xd7ef821e, "current_task" },
	{ 0x9e0eb7fb, "debugfs_create_file" },
	{ 0xfbedb4f9, "platform_device_put" },
	{ 0xfaf0539d, "platform_device_add" },
	{ 0xb6299b6b, "platform_device_alloc" },
	{ 0x9ae13cea, "platform_driver_register" },
	{ 0x7eddaad1, "dev_set_drvdata" },
	{ 0xd7b25a99, "register_framebuffer" },
	{ 0x7a890c8, "fb_alloc_cmap" },
	{ 0xdc83fe79, "framebuffer_alloc" },
	{ 0xa0b04675, "vmalloc_32" },
	{ 0xf09c7f68, "__wake_up" },
	{ 0x362ef408, "_copy_from_user" },
	{ 0x17938340, "remap_pfn_range" },
	{ 0x3744cf36, "vmalloc_to_pfn" },
	{ 0xeb0e3ef, "framebuffer_release" },
	{ 0x98b71c6, "fb_dealloc_cmap" },
	{ 0xa55d63e5, "unregister_framebuffer" },
	{ 0xad61b523, "dev_get_drvdata" },
	{ 0x999e8297, "vfree" },
	{ 0xa28da5b6, "vmalloc_to_page" },
	{ 0x50eedeb8, "printk" },
	{ 0xb3beff26, "debugfs_remove" },
	{ 0x282a088a, "platform_driver_unregister" },
	{ 0x29a09576, "platform_device_unregister" },
	{ 0xb4390f9a, "mcount" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=sysimgblt,syscopyarea,sysfillrect,fb_sys_fops";


MODULE_INFO(srcversion, "C2B4BABC46AA702002FD318");
