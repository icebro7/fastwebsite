import { createHtmlPlugin } from 'vite-plugin-html'

export function configHtmlPlugin(viteEnv, isBuild) {
  // 标题修改在.env文件
  const { VITE_TITLE } = viteEnv

  const htmlPlugin = createHtmlPlugin({
    minify: isBuild,
    inject: {
      data: {
        title: VITE_TITLE,
      },
    },
  })
  return htmlPlugin
}
