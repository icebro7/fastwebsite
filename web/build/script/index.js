import chalk from 'chalk'
import { runBuildCNAME } from './build-cname'

/**
 * @description: 调用 runBuildCNAME 函数来构建 CNAME 文件，并在构建成功或失败时输出相应的信息
 */
export const runBuild = async () => {
  try {
    runBuildCNAME()
    console.log(`✨ ${chalk.cyan('build successfully!')}`)
  } catch (error) {
    console.log(chalk.red('vite build error:\n' + error))
    process.exit(1)
  }
}

runBuild()
