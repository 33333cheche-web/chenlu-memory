// 云开发配置
wx.cloud.init({
  env: 'your-env-id', // 后续替换为你的云开发环境ID
  traceUser: true
})

const db = wx.cloud.database()
const _ = db.command

App({
  onLaunch() {
    console.log('轻笔记启动！')
    
    // 检查登录状态
    this.checkLogin()
    
    // 初始化数据
    this.initData()
  },

  // 检查登录状态
  checkLogin() {
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: (res) => {
              this.globalData.userInfo = res.userInfo
            }
          })
        }
      }
    })
  },

  // 初始化数据（本地+云端）
  initData() {
    // 先加载本地数据（快速显示）
    const localNotes = wx.getStorageSync('notes') || []
    
    // 然后同步云端数据
    this.syncFromCloud()
  },

  // 从云端同步数据到本地
  syncFromCloud() {
    const openid = wx.getStorageSync('openid')
    if (!openid) return

    db.collection('notes')
      .where({ _openid: openid })
      .orderBy('updateTime', 'desc')
      .get()
      .then(res => {
        const cloudNotes = res.data.map(item => ({
          id: item._id,
          type: item.type,
          content: item.content,
          category: item.category,
          completed: item.completed,
          createTime: item.createTime,
          updateTime: item.updateTime,
          synced: true
        }))
        
        // 合并本地和云端数据（以云端为准）
        wx.setStorageSync('notes', cloudNotes)
        
        // 通知页面刷新
        if (this.refreshCallback) {
          this.refreshCallback()
        }
      })
      .catch(err => {
        console.error('同步失败:', err)
      })
  },

  // 保存数据到云端
  saveToCloud(note) {
    const openid = wx.getStorageSync('openid')
    if (!openid) {
      // 未登录，只存本地
      return Promise.resolve()
    }

    return db.collection('notes').add({
      data: {
        type: note.type,
        content: note.content,
        category: note.category,
        completed: note.completed || false,
        createTime: note.createTime,
        updateTime: note.updateTime,
        _openid: openid
      }
    })
  },

  // 更新云端数据
  updateInCloud(id, data) {
    return db.collection('notes').doc(id).update({
      data: {
        ...data,
        updateTime: Date.now()
      }
    })
  },

  // 删除云端数据
  deleteFromCloud(id) {
    return db.collection('notes').doc(id).remove()
  },

  globalData: {
    userInfo: null,
    openid: null,
    isLogin: false
  }
})