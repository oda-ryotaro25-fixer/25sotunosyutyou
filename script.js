// スムーズスクロールとナビゲーション機能
document.addEventListener('DOMContentLoaded', function () {
  // サイドナビゲーション
  const sideNav = document.getElementById('sideNav')
  const navToggle = document.getElementById('navToggle')
  const mainContent = document.querySelector('.main-content')
  const navLinks = document.querySelectorAll('.nav-link')

  // ナビゲーショントグル
  navToggle.addEventListener('click', function () {
    sideNav.classList.toggle('collapsed')
    mainContent.classList.toggle('full-width')
  })

  // スムーズスクロール
  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault()
      const targetId = this.getAttribute('href')
      const targetSection = document.querySelector(targetId)

      if (targetSection) {
        const offset = 20
        const targetPosition = targetSection.offsetTop - offset

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth',
        })

        // アクティブクラスの更新
        navLinks.forEach(l => l.classList.remove('active'))
        this.classList.add('active')
      }
    })
  })

  // スクロール位置に応じたナビゲーションのハイライト
  const sections = document.querySelectorAll('.section')
  const observerOptions = {
    threshold: 0.3,
    rootMargin: '-20% 0px -70% 0px',
  }

  const sectionObserver = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id')
        navLinks.forEach(link => {
          link.classList.remove('active')
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active')
          }
        })
      }
    })
  }, observerOptions)

  sections.forEach(section => {
    sectionObserver.observe(section)
  })

  // 読書プログレスバー
  const progressBar = document.getElementById('progressBar')
  const readingProgress = document.getElementById('readingProgress')

  function updateProgressBar() {
    const scrollTop = window.pageYOffset
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = (scrollTop / docHeight) * 100

    progressBar.style.width = progress + '%'
    if (readingProgress) {
      readingProgress.style.width = progress + '%'
    }
  }

  window.addEventListener('scroll', updateProgressBar)

  // スクロールトップボタン
  const scrollTopButton = document.getElementById('scrollTop')

  window.addEventListener('scroll', function () {
    if (window.pageYOffset > 300) {
      scrollTopButton.classList.add('visible')
    } else {
      scrollTopButton.classList.remove('visible')
    }
  })

  scrollTopButton.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  })

  // 画像の遅延読み込み
  const images = document.querySelectorAll('.figure')
  const imageOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px 50px 0px',
  }

  const imageObserver = new IntersectionObserver(function (entries, observer) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.classList.add('loaded')
        observer.unobserve(img)
      }
    })
  }, imageOptions)

  images.forEach(img => {
    imageObserver.observe(img)
  })

  // モバイル対応
  let touchStartX = 0
  let touchEndX = 0

  document.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX
  })

  document.addEventListener('touchend', function (e) {
    touchEndX = e.changedTouches[0].screenX
    handleSwipe()
  })

  function handleSwipe() {
    if (touchEndX < touchStartX - 50) {
      // 左スワイプ - ナビを閉じる
      sideNav.classList.add('collapsed')
    }
    if (touchEndX > touchStartX + 50) {
      // 右スワイプ - ナビを開く
      sideNav.classList.remove('collapsed')
    }
  }
})
