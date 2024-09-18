import { request } from '@/utils'

/**
 * @description: 通过request与后端通信，提高了代码的可维护性和稳定性
 */
export default {
  // 用户登录，获取访问令牌
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),

  // 获取用户信息
  getUserInfo: () => request.get('/base/userinfo'),

  // 获取用户菜单
  getUserMenu: () => request.get('/base/usermenu'),

  // 获取用户API权限
  getUserApi: () => request.get('/base/userapi'),

  // 更新用户密码
  updatePassword: (data = {}) => request.post('/base/update_password', data),

  // 获取用户列表
  getUserList: (params = {}) => request.get('/user/list', { params }),

  // 根据ID获取用户信息
  getUserById: (params = {}) => request.get('/user/get', { params }),

  // 创建新用户
  createUser: (data = {}) => request.post('/user/create', data),

  // 更新用户信息
  updateUser: (data = {}) => request.post('/user/update', data),

  // 删除用户
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),

  // 获取角色列表
  getRoleList: (params = {}) => request.get('/role/list', { params }),

  // 创建新角色
  createRole: (data = {}) => request.post('/role/create', data),

  // 更新角色信息
  updateRole: (data = {}) => request.post('/role/update', data),

  // 删除角色
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),

  // 更新角色授权
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),

  // 获取角色授权信息
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),

  // 获取菜单列表
  getMenus: (params = {}) => request.get('/menu/list', { params }),

  // 创建新菜单
  createMenu: (data = {}) => request.post('/menu/create', data),

  // 更新菜单信息
  updateMenu: (data = {}) => request.post('/menu/update', data),

  // 删除菜单
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),

  // 获取API列表
  getApis: (params = {}) => request.get('/api/list', { params }),

  // 创建新API
  createApi: (data = {}) => request.post('/api/create', data),

  // 更新API信息
  updateApi: (data = {}) => request.post('/api/update', data),

  // 删除API
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),

  // 刷新API数据
  refreshApi: (data = {}) => request.post('/api/refresh', data),

  // 获取部门列表
  getDepts: (params = {}) => request.get('/dept/list', { params }),

  // 创建新部门
  createDept: (data = {}) => request.post('/dept/create', data),

  // 更新部门信息
  updateDept: (data = {}) => request.post('/dept/update', data),

  // 删除部门
  deleteDept: (params = {}) => request.delete('/dept/delete', { params }),

  // 获取审计日志列表
  getAuditLogList: (params = {}) => request.get('/auditlog/list', { params }),
}
