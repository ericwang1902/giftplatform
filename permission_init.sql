START TRANSACTION;
/*管理员权限项目初始化*/
INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list user',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'list_userprofile') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_userprofile'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change user',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'change_userprofile') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_userprofile'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add user',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'add_userprofile') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_userprofile'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete user',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'delete_userprofile') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_userprofile'
) LIMIT 1;
/*******************/



/*管理角色权限项目初始化*/

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list group',(SELECT id FROM django_content_type WHERE model='group' LIMIT 1), 'list_group') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_group'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change group',(SELECT id FROM django_content_type WHERE model='group' LIMIT 1), 'change_group') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_group'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add group',(SELECT id FROM django_content_type WHERE model='group' LIMIT 1), 'add_group') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_group'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete group',(SELECT id FROM django_content_type WHERE model='group' LIMIT 1), 'delete_group') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_group'
) LIMIT 1;

/*******************/

/*管理供应商权限项目初始化*/
INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list supplier',(SELECT id FROM django_content_type WHERE model='supplier' LIMIT 1), 'list_supplier') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_supplier'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change supplier',(SELECT id FROM django_content_type WHERE model='supplier' LIMIT 1), 'change_supplier') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_supplier'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add supplier',(SELECT id FROM django_content_type WHERE model='supplier' LIMIT 1), 'add_supplier') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_supplier'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete supplier',(SELECT id FROM django_content_type WHERE model='supplier' LIMIT 1), 'delete_supplier') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_supplier'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can auth supplier',(SELECT id FROM django_content_type WHERE model='supplier' LIMIT 1), 'auth_supplier') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='auth_supplier'
) LIMIT 1;
/*******************/

/*管理礼品公司权限项目初始化*/
INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list giftdealer',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'list_giftdealer') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_giftdealer'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change giftdealer',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'change_giftdealer') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_giftdealer'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add giftdealer',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'add_giftdealer') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_giftdealer'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete giftdealer',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'delete_giftdealer') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_giftdealer'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can auth giftdealer',(SELECT id FROM django_content_type WHERE model='userprofile' LIMIT 1), 'auth_giftdealer') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='auth_giftdealer'
) LIMIT 1;

/*******************/

/*商品分组权限初始化*/

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list category',(SELECT id FROM django_content_type WHERE model='category' LIMIT 1), 'list_category') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_category'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change category',(SELECT id FROM django_content_type WHERE model='category' LIMIT 1), 'change_category') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_category'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add category',(SELECT id FROM django_content_type WHERE model='category' LIMIT 1), 'add_category') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_category'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete category',(SELECT id FROM django_content_type WHERE model='category' LIMIT 1), 'delete_category') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_category'
) LIMIT 1;

/*******************/

/*商品品牌管理权限初始化*/
INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list brands',(SELECT id FROM django_content_type WHERE model='brands' LIMIT 1), 'list_brands') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_brands'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change brands',(SELECT id FROM django_content_type WHERE model='brands' LIMIT 1), 'change_brands') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_brands'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add brands',(SELECT id FROM django_content_type WHERE model='brands' LIMIT 1), 'add_brands') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_brands'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete brands',(SELECT id FROM django_content_type WHERE model='brands' LIMIT 1), 'delete_brands') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_brands'
) LIMIT 1;

/*******************/

/*商品场景管理权限初始化*/
INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list scene',(SELECT id FROM django_content_type WHERE model='scene' LIMIT 1), 'list_scene') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_scene'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change scene',(SELECT id FROM django_content_type WHERE model='scene' LIMIT 1), 'change_scene') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_scene'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add scene',(SELECT id FROM django_content_type WHERE model='scene' LIMIT 1), 'add_scene') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_scene'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete scene',(SELECT id FROM django_content_type WHERE model='scene' LIMIT 1), 'delete_scene') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_scene'
) LIMIT 1;
/*******************/

/*私有域管理权限初始化*/
INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can list privatearea',(SELECT id FROM django_content_type WHERE model='privatearea' LIMIT 1), 'list_privatearea') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='list_privatearea'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can change privatearea',(SELECT id FROM django_content_type WHERE model='privatearea' LIMIT 1), 'change_privatearea') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='change_privatearea'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can add privatearea',(SELECT id FROM django_content_type WHERE model='privatearea' LIMIT 1), 'add_privatearea') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='add_privatearea'
) LIMIT 1;

INSERT INTO auth_permission(name, content_type_id, codename)
SELECT * FROM (SELECT 'Can delete privatearea',(SELECT id FROM django_content_type WHERE model='privatearea' LIMIT 1), 'delete_privatearea') AS tmp
WHERE NOT EXISTS (
	SELECT * FROM auth_permission WHERE codename='delete_privatearea'
) LIMIT 1;
/*******************/


select * from auth_permission;
