const app = getApp()
const db = wx.cloud.database()

Page({
  data: {
    currentMode: 'note',
    inputContent: '',
    currentCategory: '',
    categories: [
      { id: 'work', name: '工作', icon: '💼', desc: '项目笔记与待办', count: 0 },
      { id: 'life', name: '生活', icon: '🏠', desc: '日常琐事记录', count: 0 },
      { id: 'inspiration', name: '随笔', icon: '✨', desc: '收集灵感和碎碎念', count: 0 }
    ],
    tempTasks: [{ content: '', completed: false }],
    recentNotes: [],
    showCategoryPopup: false,
    isLogin: false,
    openid: '',
    syncStatus: '未同步'
  },

  onLoad() {
    // 检查登录状态
    this.checkLogin()
  },

  onShow() {
    this.loadData()
  },

  // 检查登录并获取 openid
  checkLogin() {
    wx.cloud.callFunction({
      name: 'login'
    }).then(res => {
      const openid = res.result.openid
      wx.setStorageSync('openid', openid)
      this.setData({ 
        isLogin: true, 
        openid,
        syncStatus: '已登录'
      })
      // 登录后同步云端数据
      this.syncFromCloud()
    }).catch(err => {
      console.log('未登录', err)
      this.setData({ syncStatus: '未登录' })
      // 未登录时只加载本地数据
      this.loadLocalData()
    })
  },

  // 从云端同步数据
  syncFromCloud() {
    this.setData({ syncStatus: '同步中...' })
    
    db.collection('notes')
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
        
        // 保存到本地
        wx.setStorageSync('notes', cloudNotes)
        this.updateUI(cloudNotes)
        this.setData({ syncStatus: '已同步' })
        
        wx.showToast({ title: '同步成功', icon: 'success' })
      })
      .catch(err => {
        console.error('同步失败', err)
        this.setData({ syncStatus: '同步失败' })
        this.loadLocalData()
      })
  },

  // 加载本地数据
  loadLocalData() {
    const notes = wx.getStorageSync('notes') || []
    this.updateUI(notes)
  },

  // 加载数据（优先云端）
  loadData() {
    if (this.data.isLogin) {
      this.syncFromCloud()
    } else {
      this.loadLocalData()
    }
  },

  // 更新UI
  updateUI(notes) {
    // 更新分类计数
    const categories = this.data.categories.map(cat => {
      const count = notes.filter(n => n.category === cat.name).length
      return { ...cat, count }
    })

    // 获取最近3条
    const recentNotes = notes
      .sort((a, b) => b.updateTime - a.updateTime)
      .slice(0, 3)
      .map(note => ({
        ...note,
        timeText: this.formatTime(note.updateTime)
      }))

    this.setData({ categories, recentNotes })
  },

  formatTime(timestamp) {
    const now = Date.now()
    const diff = now - timestamp
    if (diff < 3600000) return '刚刚'
    if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
    return Math.floor(diff / 86400000) + '天前'
  },

  // 切换模式
  switchMode(e) {
    this.setData({ currentMode: e.currentTarget.dataset.mode })
  },

  onInput(e) {
    this.setData({ inputContent: e.detail.value })
  },

  addTempTask() {
    const tasks = this.data.tempTasks
    if (tasks[tasks.length - 1].content === '') {
      wx.showToast({ title: '请先填写当前任务', icon: 'none' })
      return
    }
    tasks.push({ content: '', completed: false })
    this.setData({ tempTasks: tasks })
  },

  onTaskInput(e) {
    const idx = e.currentTarget.dataset.index
    const val = e.detail.value
    const tasks = this.data.tempTasks
    tasks[idx].content = val
    this.setData({ tempTasks: tasks })
  },

  toggleTempTask(e) {
    const idx = e.currentTarget.dataset.index
    const tasks = this.data.tempTasks
    tasks[idx].completed = !tasks[idx].completed
    this.setData({ tempTasks: tasks })
  },

  selectCategory() {
    this.setData({ showCategoryPopup: true })
  },

  closeCategoryPopup() {
    this.setData({ showCategoryPopup: false })
  },

  confirmCategory(e) {
    this.setData({ 
      currentCategory: e.currentTarget.dataset.name,
      showCategoryPopup: false
    })
  },

  // 保存笔记（本地+云端）
  saveContent() {
    const { currentMode, inputContent, tempTasks, currentCategory, isLogin } = this.data
    
    if (!currentCategory) {
      wx.showToast({ title: '请先选择分类', icon: 'none' })
      return
    }

    let noteData = {
      type: currentMode,
      category: currentCategory,
      completed: false,
      createTime: Date.now(),
      updateTime: Date.now()
    }

    if (currentMode === 'note') {
      if (!inputContent.trim()) {
        wx.showToast({ title: '请输入内容', icon: 'none' })
        return
      }
      noteData.content = inputContent
    } else {
      const validTasks = tempTasks.filter(t => t.content.trim())
      if (validTasks.length === 0) {
        wx.showToast({ title: '请至少添加一个任务', icon: 'none' })
        return
      }
      noteData.content = validTasks.map(t => `${t.completed ? '[x]' : '[ ]'} ${t.content}`).join('\n')
      noteData.tasks = validTasks
    }

    // 先保存本地
    const notes = wx.getStorageSync('notes') || []
    noteData.id = 'local_' + Date.now()
    notes.unshift(noteData)
    wx.setStorageSync('notes', notes)

    // 如果已登录，同步到云端
    if (isLogin) {
      this.setData({ syncStatus: '保存中...' })
      
      db.collection('notes').add({
        data: noteData
      }).then(res => {
        // 更新本地id为云端id
        noteData.id = res._id
        noteData.synced = true
        const newNotes = wx.getStorageSync('notes')
        newNotes[0] = noteData
        wx.setStorageSync('notes', newNotes)
        
        this.setData({ syncStatus: '已同步' })
        wx.showToast({ title: '保存成功', icon: 'success' })
      }).catch(err => {
        console.error('云端保存失败', err)
        wx.showToast({ title: '已保存本地', icon: 'none' })
        this.setData({ syncStatus: '同步失败' })
      })
    } else {
      wx.showToast({ title: '已保存本地', icon: 'success' })
    }

    // 重置
    this.setData({
      inputContent: '',
      tempTasks: [{ content: '', completed: false }],
      currentCategory: ''
    })

    this.loadData()
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.syncFromCloud()
    wx.stopPullDownRefresh()
  },

  editNote(e) {
    wx.navigateTo({
      url: `/pages/detail/detail?id=${e.currentTarget.dataset.id}`
    })
  },

  goToCategory(e) {
    wx.showToast({ title: '分类详情开发中', icon: 'none' })
  }
})