## v0.19.7

- Update submodules

- 修复: 移除未使用的Ref参数警告

- - config_provider.dart: 移除ConfigStateNotifier中未使用的_ref参数
- - latency_service.dart: 移除LatencyService中未使用的_ref参数
- - 清理构造函数参数，消除IDE警告
- - 保持代码功能不变

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 优化: 代码格式化和清理优化

- - 移除未使用的imports和方法
- - 统一代码格式化
- - 清理冗余代码，提升代码质量
- - 优化文件结构和可读性

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 重构: 拆分InvitePage巨大文件，提升代码可维护性

- - 将1222行的invite_page.dart重构为88行的主页面
- - 提取5个对话框组件到独立文件:
-   * ThemeDialog - 主题选择对话框
-   * LogoutDialog - 登出确认对话框
-   * WithdrawDialog - 提现对话框
-   * TransferDialog - 转账对话框
-   * CommissionHistoryDialog - 佣金历史对话框
- - 提取8个卡片组件到独立widget:
-   * UserMenuWidget - 用户菜单组件
-   * ErrorCard - 错误提示卡片
-   * InviteRulesCard - 邀请规则卡片
-   * InviteQrCard - 邀请码二维码卡片
-   * InviteStatsCard - 统计信息卡片
-   * WalletDetailsCard - 钱包详情卡片
-   * CommissionHistoryCard - 佣金历史卡片
-   * StatItemWidget - 统计项显示组件

- 优势:
- - 单一职责原则，每个组件功能清晰
- - 代码复用性提升，便于单元测试
- - 提升代码可读性和可维护性
- - 减少主页面代码量93%

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 修复: 解决重复调用/api/v1/user/getSubscribe的问题

- ## 问题分析
- - refreshSubscriptionInfo() 错误包含支付成功逻辑
- - 每次刷新订阅信息都会额外触发订阅导入
- - 与SubscriptionStatusChecker形成重复调用

- ## 解决方案

- ### 🔧 分离支付逻辑
- - 创建 `refreshSubscriptionInfoAfterPayment()` 处理支付成功场景
- - 简化 `refreshSubscriptionInfo()` 只负责刷新信息
- - 修正支付成功回调使用正确的方法

- ### 🛡️ 添加去重机制
- - 在 `SimpleSubscriptionService` 中集成 `OperationCoordinator`
- - 防止重复的 importSubscription/updateSubscription 操作
- - 同时触发的请求会复用第一个操作的结果

- ### 📊 优化后效果
- - 去重机制正常工作: `[OperationCoordinator] 操作正在进行中，复用结果`
- - API调用变得合理: 每个调用都有明确目的
- - 流量信息正常显示: 订阅信息正确设置

- ## 技术实现
- - 支付成功: `refreshSubscriptionInfoAfterPayment()` → 刷新 + 强制更新
- - 普通刷新: `refreshSubscriptionInfo()` → 只获取信息
- - 去重保护: 所有导入操作通过 `OperationCoordinator` 统一管理

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 重构: 彻底简化XBoard订阅管理，修复流量信息显示问题

- ## 主要改进

- ### 🗑️ 删除复杂系统
- - 删除 `subscription_manager.dart` (679行复杂代码)
- - 移除复杂的优先级、节流、去重逻辑
- - 清理相关导出和依赖

- ### ✨ 简化实现
- - 创建 `SimpleSubscriptionService` (仅96行代码)
- - 只保留两个核心方法：`importSubscription()` 和 `updateSubscription()`
- - 直接使用主项目的 `Profile.normal()` 和 `profilesProvider`

- ### 🔧 修复流量信息显示
- - 集成 `ProfileSubscriptionInfoService` 获取订阅信息
- - 确保创建的Profile包含完整的subscriptionInfo
- - 修复导入后不显示已用流量的问题

- ### 📝 统一调用接口
- - 提供简洁的扩展方法：`ref.importSubscription()` 和 `ref.updateSubscription()`
- - 支持 WidgetRef 和 NotifierProviderRef 两种类型
- - 替换所有复杂的 `requestImport` 调用

- ## 技术细节
- - 导入时先删除所有现有配置，再创建新配置
- - 自动获取和设置订阅信息(upload/download/total/expire)
- - 保持代码简洁，符合"就很简单"的设计理念

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 重构: 简化订阅导入接口，统一调用方式

- - 新增语义化的高级API方法：
-   - updateSubscription() - 手动刷新
-   - importOnStartup() - 启动时导入
-   - importAfterLogin() - 登录后导入
-   - forceUpdateAfterPayment() - 支付后强制更新
-   - importByUser() - 用户手动导入
-   - importAfterStatusCheck() - 状态检查后导入
- - 替换所有 requestImport 调用为对应的高级API
- - 简化了调用代码，减少参数配置错误

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 优化: 添加操作协调器解决XBoard重复流程问题

- - 新增 OperationCoordinator 类提供防重复和防抖机制
- - 订阅管理器集成协调器，解决多次重复导入问题
- - 延迟测试服务添加防抖处理，避免快速切换时的重复测试
- - 支持高优先级操作中断低优先级操作
- - 保持向后兼容，最小化架构侵入

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 修复: 解决加密订阅导入后profile卡片不显示流量信息的问题

- 主要修复:
- - 修复SubscriptionManager在处理加密订阅时未设置subscriptionInfo的问题
- - 修复ProfileImportService的_downloadEncryptedProfile方法订阅信息缺失
- - 创建ProfileSubscriptionInfoService统一处理订阅信息获取逻辑
- - 完善EncryptedSubscriptionService支持获取subscription-userinfo响应头

- 技术改进:
- - 重构订阅信息获取逻辑，避免代码重复
- - 统一错误处理和回退机制（XBoard API -> subscription-userinfo -> 空对象）
- - 移除调试日志，优化代码结构
- - 确保加密订阅和普通订阅都能正确显示流量使用信息

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 重构: 统一订阅导入管理器，解决重复导入问题

- ## 主要改进
- - 创建统一的 SubscriptionManager 管理所有订阅导入
- - 实现智能去重和节流机制，避免重复导入
- - 修复从登录数据获取订阅后未实际创建配置文件的问题
- - 优化配置清理逻辑，确保只保留最新配置

- ## 技术细节
- - 新增 SubscriptionManager 类，统一管理导入策略
- - 支付成功、登录后、状态检查等场景使用统一入口
- - 修复 XBoardSDK user 属性缺失问题 (user → userInfo)
- - 修复类型转换错误 (UserInfo → Map<String, dynamic>)
- - 优化 token 获取逻辑，优先从订阅信息获取正确 token

- ## 导入策略
- - 支付成功: 高优先级，强制刷新，5秒去重
- - 登录后: 中优先级，5秒节流，60秒去重
- - 状态检查: 中优先级，10秒节流，30秒去重
- - 应用启动: 低优先级，30秒节流，120秒去重

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 优化: 完善XBoard系统模块日志管理

- - 统一system目录下所有模块使用SystemLogger日志系统
- - 更新remote_task、online_support、update_check、domain_status、latency模块
- - 替换所有print()和debugPrint()调用为统一的日志接口
- - 清理冗余的示例文件和文档
- - 优化日志级别分类：info、debug、warning、error

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 优化: 重构XBoard日志系统，统一日志管理

- - 创建统一的XBoard日志系统，支持模块化日志管理
- - 重构所有XBoard模块以使用新的日志系统
- - 删除测试文件和冗余的README
- - 优化错误处理和配置解析模块

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 修复: 修复SubscriptionUrlHelper缺失方法导致的编译错误

- - 重新实现SubscriptionUrlHelper类，添加缺失的initialize()和transformUrl()方法
- - 完善订阅URL解析和处理功能，支持多种URL格式
- - 新增加密订阅服务支持，包括解密工具和服务类
- - 扩展XBoard配置系统以支持订阅信息管理
- - 添加订阅URL提取、验证和标准化功能

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 优化: 统一应用名称为WuJie并解除窗口固定大小限制

- - 将应用名称从"无界"改为"WuJie"保持英文一致性
- - 修改macOS应用包名称为WuJie.app
- - 解除窗口固定大小限制，允许用户自由调整窗口尺寸
- - 设置合理的最小窗口尺寸(600x500)防止窗口过小

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

## v2.6.0_wujie-official

- 优化: Windows自建runner跳过Flutter下载直接使用本机安装

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

## v2.6.0_wujie_official

- 发布: v2.6.0无界官方版本

- - 优化Windows构建流程，移除Go setup action缓存上传延迟
- - 应用无界品牌化修改（应用名称、标识等）
- - 合并test-windows-build分支的所有优化

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- Merge branch 'test-windows-build'

- 优化: 移除Go setup action避免缓存上传延迟

- - 将 actions/setup-go@v5 替换为直接验证已安装的Go
- - 避免在自托管runner上进行Go缓存的上传/下载
- - 减少post-setup阶段的时间消耗
- - 保持现有的Flutter验证策略

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: Windows平台使用自建runner

- - 将Windows构建改为使用self-hosted runner
- - 为Windows平台明确指定bash shell
- - 保持其他平台使用GitHub hosted runners

- 这样可以利用已配置好的Windows构建环境和工具缓存

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 恢复完整的多平台CI/CD，仅改进Windows构建部分

- - 恢复原有的多平台构建支持（Windows、macOS、Android、Linux）
- - 保留完整的changelog和upload工作流程
- - 仅在Windows平台添加改进的构建环境配置：
-   * 优化工具安装和缓存（jq、Rust、VS Build Tools、Inno Setup）
-   * 添加flutter_distributor支持
-   * 改进PATH配置和错误处理
- - 修复之前错误覆盖整个CI/CD配置的问题

- 这是正确的集成方式：保持多平台支持，只增强Windows部分

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- merge: 合并test-windows-build分支到main

- 包含以下重要修复和改进：

- 1. Windows构建流程优化：
-    - 添加Inno Setup支持，生成Windows安装程序
-    - 优化Visual Studio Build Tools安装
-    - 改进工具缓存机制（jq, Rust, VS Build Tools等）

- 2. 应用功能修复：
-    - 修复User-Agent中文字符导致订阅导入失败
-    - 修复WebSocket SSL证书验证问题
-    - 改进订阅导入失败的用户提示

- 3. 构建工具改进：
-    - 添加UTF-8解码错误处理
-    - 优化构建输出检查和日志
-    - 改进自建runner的工具安装和缓存

- 解决应用名称冲突：保持main分支设置(FlClash)

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复jq二进制文件执行错误

- - 优先使用chocolatey安装jq（更可靠）
- - 添加文件完整性检查（使用-s标志）
- - 改进错误处理和PATH管理
- - 添加执行权限设置
- - 提供详细的安装状态反馈

- 解决了'cannot execute binary file: Exec format error'问题

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复订阅导入和WebSocket连接问题

- 1. 修复User-Agent中文字符导致HTTP头格式错误
-    - 将User-Agent中的中文应用名改为英文版本
-    - 解决"Invalid HTTP header field value"错误

- 2. 修复WebSocket SSL证书验证失败问题
-    - 为WebSocket连接添加SSL证书跳过配置
-    - 解决"CERTIFICATE_VERIFY_FAILED"错误

- 3. 改进订阅导入失败的用户提示
-    - 特殊处理HTTP格式错误，显示用户友好的提示
-    - 简化技术错误信息，避免显示复杂的技术细节

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 添加Inno Setup支持，修复Windows安装程序生成问题

- - 在CI workflow中添加Inno Setup自动安装
- - 配置PATH环境变量包含Inno Setup编译器
- - 添加构建工具验证步骤
- - 改进构建输出检查，专门寻找.exe/.zip/.msi文件
- - 添加flutter_distributor日志检查

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 添加Visual Studio Build Tools ATL组件检查，避免重复安装

- - 添加ATL头文件存在性检查，如已安装则跳过
- - 优先尝试修改现有Build Tools安装添加ATL组件
- - 修改失败时fallback到完整重新安装
- - 优化安装流程，减少构建时间

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 改进Visual Studio Build Tools安装，修复ATL头文件缺失问题

- - 使用winget替代chocolatey进行Visual Studio Build Tools安装
- - 添加Microsoft.VisualStudio.Component.VC.ATL和VC.ATLMFC组件
- - 添加Windows10SDK.20348组件确保完整的构建环境
- - 增加ATL头文件验证步骤，确保atlstr.h正确安装
- - 提供chocolatey备用安装方案

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修改VS Build Tools安装为bash脚本，避免PowerShell执行策略问题

- fix: 修复workflow语法错误，移除无效的success()函数调用

- fix: 添加Visual Studio Build Tools安装，解决ATL头文件缺失问题

- debug: 添加详细的构建输出检查，查找所有可能的文件名

- fix: 移除Upload的条件检查，添加更详细的调试信息

- fix: 添加构建环境准备和输出检查，确保flutter_distributor可用

- fix: 添加Pub Cache bin路径到PATH，解决flutter_distributor命令找不到的问题

- fix: 添加Rust/Cargo自动安装，解决构建依赖问题

- fix: 修复setup.dart中的UTF-8解码异常，添加编码错误处理

- fix: 修复bash环境下的路径切换命令，使用cd替代Set-Location

- fix: 移除flutter-action，使用预安装的Flutter避免下载卡死

- fix: 使用国内镜像源解决Flutter下载网络问题

- fix: 将jq安装脚本改为bash版本

- fix: 添加jq工具安装步骤，解决flutter-action依赖问题

- revert: 恢复flutter-action配置，准备在runner上安装bash

- fix: 移除flutter-action，使用预安装的Flutter SDK

- fix: 修复Windows自建runner的shell问题，使用PowerShell替代bash

- fix: 修复macOS构建错误并统一应用名称为WuJie

- - 修复package.dart中appNameEn不存在的错误，改为使用appName
- - 统一macOS配置文件中的应用名称为WuJie
- - 更新Xcode项目文件中的所有应用名称引用
- - 确保DMG配置和Scheme文件一致

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 修改工作流仅构建Windows版本，使用自建runner

- feat: 合并test-windows-build分支，修改应用名称为wujie

- - 更新应用名称为wujie
- - 修复Windows安装器名称显示问题
- - 调整打包配置文件
- - 更新CI/CD工作流配置

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 修改应用名称为wujie

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 修改应用名称为wujie

- - 修改Windows项目名称和可执行文件名为wujie
- - 修改资源文件中的应用名称为wujie
- - 修改setup.dart中的应用名称
- - 修改distribute_options.yaml中的应用名称
- - 确保安装器创建的文件夹名为wujie，快捷方式为wujie.exe

- feat: 创建Windows测试分支，修复安装器名称显示问题

- - 修改构建工作流只打包Windows平台
- - 修复Windows资源文件中的应用名称为'无界畅游'
- - 修复setup.dart中的应用名称
- - 修复distribute_options.yaml中的应用名称
- - 确保Windows安装器显示正确的应用名称

- feat: 恢复应用名称为 FlClash

- - 将所有平台应用名称从「无界畅游」改回 FlClash
- - 修改 Android strings.xml 中的应用名称
- - 修改 Windows/Linux CMakeLists.txt 中的项目名称
- - 修改 macOS AppInfo.xcconfig 中的产品名称
- - 修改应用常量中的显示名称
- - 保持程序代码中的关键字不变

- Add Swift Package Manager cache cleanup for macOS builds

- Add Swift Package Manager cache cleanup for macOS builds

- Release v2.6.0_wujie_official: fix macOS DMG packaging, remove Linux ARM, enable release upload

- use debug sign

- Disable ARM builds to reduce build time and improve stability

- Optimize build order: Windows first, then macOS

- Fix SDK code generation order in CI

- Add code generation step to fix CI build

- Disable distribution, keep build artifacts only

- fix: improve image picker widget layout and prevent overflow

- - Add responsive height constraints to prevent layout overflow
- - Improve scrollable content area with proper padding
- - Remove third line text to simplify UI and fix bottom spacing
- - Add better space calculation for different screen sizes
- - Use Flexible and SingleChildScrollView for better layout handling

- feat: change default theme mode to system

- feat: internationalize update_check and online_support features

- - Add i18n support for update_check feature:
-   - Internationalize UpdateDialog with version info and release notes
-   - Internationalize UpdateService error messages
-   - Add translations for 12 keys in zh_CN, en, ja, ru

- - Add i18n support for online_support feature:
-   - Internationalize OnlineSupportPage with connection status and UI text
-   - Internationalize ImagePickerWidget with file selection and upload text
-   - Internationalize ApiService error messages
-   - Add translations for 26 keys in zh_CN, en, ja, ru

- - Fix contact support button internationalization:
-   - Replace hardcoded '联系客服' text in xboard_home_page
-   - Internationalize configuration error messages in error_handler
-   - Add contactSupport and configurationError translation keys

- All user-visible text now supports Chinese, English, Japanese, and Russian languages.

- feat: complete invite page internationalization

- - Fix all hardcoded Chinese text in invite page
- - Replace context.l10n with appLocalizations for proper i18n
- - Fix placeholder translation keys to use function calls
- - Remove const constructors with non-constant values
- - Clean up unused code and deprecation warnings
- - Support both Chinese and English with concise English translations
- - All invite features now properly internationalized:
-   - Invite rules and statistics
-   - QR code generation and display
-   - Wallet details and transfer functionality
-   - Commission history
-   - Theme switching and logout

- feat: 完成邀请页面个人中心下拉菜单和佣金历史分页功能

- ## 🎯 个人中心功能增强
- - 新增登出功能到下拉菜单
- - 保留切换主题功能
- - 添加确认对话框防止误操作
- - 使用统一的登出逻辑和状态管理

- ## 🚀 佣金历史分页系统
- - 替换瀑布渲染为高效分页机制
- - 实现自动滚动加载和手动加载更多
- - 每页显示10条记录，支持无限滚动
- - 添加分页信息显示和刷新功能
- - 优化加载状态指示器

- ## 🔧 后端接口改进
- - 修改InviteService接口支持分页参数
- - 更新domain service facade传递分页参数
- - 修复SDK调用参数匹配问题
- - 改进错误处理和类型安全

- ## 🎨 UI/UX 优化
- - 分页对话框显示页码和记录总数
- - 智能加载：接近底部自动加载下一页
- - 加载状态实时反馈
- - 保持原有UI风格一致性

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 在邀请页面右上角添加个人中心按钮

- - 添加个人中心PopupMenuButton到右上角
- - 实现主题切换功能（自动/浅色/深色）
- - 使用PageMixin和isCurrentPageProvider确保按钮稳定显示
- - 修复按钮闪烁问题，参考主页实现方式

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- style: 统一划转和提现按钮样式

- - 将划转按钮从OutlinedButton改为TextButton，与提现按钮保持一致
- - 确保钱包详情和佣金历史卡片的按钮样式统一

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现钱包划转功能和UI重构

- - 重构佣金详情为钱包详情，添加划转按钮
- - 实现完整的划转功能，包含输入验证和错误处理
- - 添加划转动画效果：加载状态、成功提示、自动关闭
- - 集成用户信息API，显示真实钱包余额
- - 修复异步操作中的widget生命周期问题
- - 优化按钮样式，确保在不同主题下可见性

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 修复邀请页面佣金数据显示和提现功能

- - 修正stat字段映射，正确解析API返回的佣金数据
- - 添加待确认佣金、佣金比例、可用佣金字段
- - 佣金金额使用k单位格式化，避免长数字破坏UI布局
- - 重构提现功能，引导用户前往网页版操作
- - 使用url_launcher直接打开网页而非复制链接
- - 在邀请规则中显示当前佣金返利比例
- - 分离邀请统计和佣金详情为独立卡片

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 重构邀请页面UI，添加二维码功能和自动邀请码生成

- - 新增二维码组件用于生成邀请链接二维码
- - 重新设计邀请页面布局：顶部邀请规则，中间二维码，底部统计
- - 实现自动邀请码生成，用户首次进入自动创建邀请码
- - 简化操作按钮：只保留保存二维码和复制链接两个功能
- - 移除复杂的邀请码管理功能，只显示主要邀请码
- - 修复邀请链接格式，正确添加前端路由#符号
- - 使用SDK初始化的base URL而不是config中的appUrl

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成邀请模块架构重构和功能实现

- - 参考其他模块设计架构，完善邀请模块结构
- - 新增 InviteProvider 状态管理，支持响应式数据更新
- - 新增 InviteService 业务逻辑封装层
- - 完善邀请页面UI，支持邀请统计、邀请码管理、佣金历史
- - 集成 domain_service SDK封装层，统一API调用
- - 支持自动数据刷新和下拉刷新
- - 移除顶部AppBar，改为页面级组件使用
- - 添加完整的错误处理和加载状态提示

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 优化移动端导航和响应式布局

- - 添加邀请页面到底部导航栏，支持邀请功能
- - 启用移动端底部导航栏，只显示主页和邀请页面
- - 精简桌面端导航栏，只保留主页、购买套餐、客服、邀请页面
- - 优化xboard主页响应式布局，根据屏幕尺寸自适应间距
- - 修改购买套餐按钮为带文本的按钮，提升用户体验
- - 减少底部导航栏高度，节省屏幕空间
- - 预留个人中心页面位置，待后续开发

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 优化套餐购买页面布局显示

- - 调整套餐卡片中流量和限速字段字体大小为12px避免超出布局
- - 简化优惠券折扣显示文字为"-¥11.00"格式

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成注册页面本地化

- - 添加注册页面相关的多语言支持
- - 完善英文和中文本地化字符串
- - 更新本地化代码生成文件

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat(i18n): Refactor Chinese localization and fix password reset page errors

- fix: 将英文语言选项图标从美国国旗改为全球图标

- - 使用 🌐 全球图标代替 🇺🇸 美国国旗
- - 提供更中性和国际化的语言选择体验

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 优化登录页面UI和语言切换功能

- - 添加中英文语言选择器组件，提供更明显的切换按钮
- - 将登录页面头部改为"无界畅游"品牌名称和域名显示
- - 调整布局：忘记密码按钮移至注册按钮上方
- - 使用地球图标替换原用户头像图标，更符合品牌定位

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现基于配置的动态注册页面

- - 新增配置Provider用于获取系统配置信息
- - 根据isEmailVerify配置动态显示邮箱验证码字段
- - 根据isInviteForce配置动态调整邀请码必填状态
- - 添加邮箱验证码发送功能和输入验证
- - 优化用户体验，空邀请码时显示友好弹窗提示
- - 支持配置加载失败时的降级处理

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 添加订阅刷新按钮

- feat: 改进忘记密码功能为两步验证流程

- - 第一步：输入邮箱发送验证码
- - 第二步：输入验证码和新密码完成重置
- - 添加表单验证和用户体验优化
- - 集成SDK的sendEmailCode和resetPassword API

- feat: 桌面端只显示xboard主页、套餐页面和在线客服

- - 修改导航配置，桌面端只显示xboard、plans和onlineSupport页面
- - 其他页面（仪表盘、代理、配置等）只在移动端显示
- - 添加onlineSupport页面标签和多语言翻译
- - 优化桌面端xboard主页，隐藏重复的联系客服按钮

- 设置窗口固定大小为850x800并禁用拖拽调整

- fix: 优化在线客服图片加载和消息处理

- - 修复图片加载超时问题，增加15秒超时时间
- - 添加更详细的网络错误日志和提示
- - 正确关闭HTTP客户端避免资源泄漏
- - 添加User-Agent头提高请求成功率
- - 简化消息重复检查逻辑，提高稳定性

- feat: 将在线客服API配置迁移到config_v2系统

- - 创建OnlineSupportInfo模型类，支持API和WebSocket URL配置
- - 创建OnlineSupportService服务类，提供配置访问接口
- - 扩展配置解析器支持在线客服配置的解析和验证
- - 在ModuleInitializer中注册OnlineSupportService
- - 更新XBoardConfigAccessor支持在线客服配置访问
- - 重构CustomerSupportServiceConfig使用新的配置系统
- - 保持向后兼容性，配置不可用时抛出异常提示
- - 支持远程配置动态更新在线客服API端点

- feat: 实现在线客服系统完整图片传送功能

- - 扩展消息模型支持附件和多种消息类型
- - 新增文件上传服务，支持图片上传和验证
- - 创建图片选择器组件，支持多文件选择和预览
- - 新增消息附件显示组件，支持图片预览和缩放
- - 扩展WebSocket服务支持附件消息发送
- - 优化聊天UI：纯图片消息无气泡，文本消息保持气泡样式
- - 添加带认证的图片加载机制解决401问题
- - 移除聊天消息时间戳，界面更简洁

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加在线客服页面WebSocket连接自动刷新机制

- - 在WebSocket服务中添加强制重连参数
- - 在ChatProvider中添加重新初始化方法
- - 在页面生命周期中添加WebSocket连接刷新逻辑
- - 确保每次进入页面都能重新建立可靠的WebSocket连接

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 全面优化在线客服聊天功能

- ## 🚀 主要改进

- ### 用户体验优化
- - ✅ 消息发送立即显示，无需等待服务器响应
- - ✅ 发送按钮显示loading状态，防止重复发送
- - ✅ 消息添加淡入滑动动画效果
- - ✅ 优化滚动行为，确保新消息可见
- - ✅ 输入框立即清空，提升交互体验

- ### API接口修复
- - 🔧 修复获取消息历史401错误：URL路径 /messages -> /messages/
- - 🔧 解决HTTP重定向导致认证头丢失问题
- - 🔧 增强所有API请求的详细调试日志
- - 🔧 统一HTTP请求处理，确保头信息正确传递

- ### WebSocket功能完善
- - 🔧 修复新消息解析：正确从message字段获取数据
- - 🔧 使用服务器返回的实际消息ID，而非本地时间戳
- - 🔧 WebSocket标记已读功能正常工作
- - 🔧 增强WebSocket消息处理调试信息

- ### 标记已读功能
- - ✅ 支持WebSocket和HTTP API双重标记方式
- - ✅ 本地状态立即更新，提升响应速度
- - ✅ 优雅降级处理，API失败不影响用户体验

- ### 代码质量
- - 📝 替换弃用的withOpacity为withValues
- - 📝 统一使用debugPrint替代print
- - 📝 添加emoji图标区分不同类型日志
- - 📝 完善异常处理和错误提示

- 🎯 修复后聊天功能完全正常，消息收发、标记已读等功能均可正常使用

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加认证Token获取功能到XBoard适配层

- - 在AuthService接口中添加getAuthToken方法
- - 在AuthServiceImpl中实现Token获取逻辑
- - 在XBoardDomainServiceFacade中暴露Token获取接口
- - 更新在线客服配置以通过适配层获取Token

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 将XBoard标题位置替换为在线客服按钮并集成完整在线客服功能

- - 扩展PageMixin支持自定义leading组件
- - 修改CommonScaffold支持动态leadingWidth设置
- - 更新AppBarState模型支持leading状态管理
- - 在XBoard页面左上角添加"联系客服"按钮，替换原标题显示
- - 集成完整的在线客服聊天系统：
-   - 实时WebSocket消息通信
-   - 消息历史记录加载
-   - 已读状态管理
-   - 聊天界面UI组件
- - 修复所有依赖路径，适配flutter_riverpod架构
- - 优化按钮布局，避免超出AppBar边界

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复XBoard配置模块编译错误并统一配置源

- - 修复XBoardService缺失的方法和属性
- - 简化域名管理逻辑，直接使用config_v2接口
- - 统一配置源管理，移除硬编码重复配置
- - 保留切换架构为后续功能扩展留出空间

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完全移除旧config模块，纯使用V2版本

- - 删除整个lib/xboard/config/目录，移除所有旧配置代码
- - 更新domain_service完全使用XBoardConfigV2 API
- - 简化XBoardService，移除旧域名提供者依赖
- - 更新domain_status_service使用V2初始化
- - 所有配置功能现在统一通过XBoardConfigV2访问

- 主要优势：
- - 代码库更简洁，无历史包袱
- - 统一的配置接口，避免API混乱
- - 更好的性能和域名选择逻辑
- - 清晰的架构分层

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 直接迁移到XBoard配置V2版本

- - 完全替换原config模块为config_v2
- - 更新main.dart和application.dart使用XBoardConfigV2 API
- - 简化配置初始化流程，移除复杂的依赖注入设置
- - 更新所有相关模块使用新的V2 API接口
- - 删除迁移适配器，直接使用V2版本
- - 修复async/await调用问题，V2 API返回直接值

- 主要变更：
- - XBoardConfigV2.initialize() 替代 initializeDI()
- - XBoardConfigV2.panelUrl 替代 XBoardConfigAPI.getEntryUrl()
- - XBoardConfigV2.wsUrl 替代 XBoardConfigAPI.getWsUrl()
- - XBoardConfigV2.updateUrl 替代 XBoardConfigAPI.getUpdateUrl()

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 重构XBoard配置模块架构

- - 将XBoardConfigAccessor移到internal文件夹，隐藏内部实现
- - 优化配置访问API，提供更清晰的公共接口
- - 改进域名选择逻辑，支持智能域名测试
- - 删除示例文件，简化代码结构
- - 更新依赖注入配置，确保组件正确注册
- - 增强错误处理和日志记录功能

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加XBoard配置系统v2

- 新增了重构的配置管理系统，包含：
- - 核心配置服务和依赖注入
- - 远程配置获取和管理
- - 配置解析和合并功能
- - 面板、代理、更新、WebSocket服务
- - 配置验证和错误处理工具
- - 全新的数据模型和架构

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 移除更新服务中的硬编码回退URL

- - 删除硬编码的 _fallbackServerUrl
- - 移除回退逻辑，配置失败时直接抛出异常
- - 简化错误处理，让原始异常直接抛出
- - 更新相关错误信息和注释

- fix: 修复节点自动延迟测试的反复测试问题

- - 修复URLTest组节点获取逻辑，正确处理组引用和真实代理节点
- - 重构_getSelectedProxyFromGroup方法，添加递归组引用处理
- - 增强缓存机制防止重复测试，添加时间窗口保护
- - 优化onNodeChanged事件处理，添加防抖机制
- - 改进错误处理和状态检查，提高系统稳定性

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 重新启用域名状态功能

- - 在登录页面右上角添加域名状态指示器
- - 只有在域名可用时才允许登录操作
- - 重构域名状态功能，符合项目架构规范:
-   - 移动到 features/system/domain_status/ 目录
-   - 实现 Provider -> Service -> API 分层架构
-   - 添加独立的状态模型和服务层
- - 清理config目录中不当放置的文件
- - 支持域名检测、状态显示和详情对话框
- - 集成现有的域名选择和测试基础设施

- feat: 远程任务模块改为非阻塞初始化

- - 远程任务模块初始化失败不再阻塞应用启动
- - 采用优雅降级策略，失败时仅禁用远程任务功能
- - 添加详细的警告日志说明功能状态
- - 提升应用启动的健壮性和用户体验

- fix: WebSocket连接URL格式修复

- - 修复WebSocket连接时缺少node_id的问题
- - 现在WebSocket URL格式为 wss://domain/ws/{node_id} 符合服务端要求
- - 添加调试信息以便排查连接问题
- - 解决403 Forbidden错误

- 简化设备信息上报机制为按需响应

- - 移除身份验证成功后的自动设备信息上报
- - 移除自动上报相关代码和方法
- - 保留device_info任务类型，只在服务器请求时响应
- - 优化为按需收集，用完即销毁，无缓存机制
- - 减少客户端资源消耗和隐私泄露风险

- 支持的服务端请求格式：
- {
-   "type": "device_info",
-   "payload": {
-     "info_type": "basic|network|system|runtime|all"
-   }
- }

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 扩展设备信息收集和自动上报功能

- - 新增DeviceInfoService服务，支持收集丰富的设备信息
- - 扩展Android设备信息：硬件、CPU架构、系统指纹等
- - 添加系统资源信息收集：CPU、内存、负载、运行时间等
- - 支持多种信息收集类型：basic、network、system、runtime、all
- - 身份验证成功后自动上报基础+系统信息
- - 所有上报和响应消息都包含nodeId关联
- - 完善错误处理和降级机制

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 修复WebSocket身份认证和消息解析问题

- - 修复WebSocketChannel.fromWebSocket不存在的错误，改用IOWebSocketChannel.connect
- - 添加web_socket_channel依赖到pubspec.yaml
- - 修复远程任务管理器中系统事件消息的解析逻辑
- - 添加对identify_ack事件的正确处理，避免格式错误
- - 改进WebSocket连接的头部认证支持

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 重构远程任务和更新检查服务从config获取端点

- - 重构RemoteTaskManager使其从XBoard配置获取WebSocket URL
- - 重构UpdateService使其从配置获取更新服务器URL
- - 支持多端点备份和自动重试机制
- - 保持向后兼容性，添加备用URL方案
- - 移除硬编码URL，实现完全配置化管理

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 更新SDK submodule - 移除HTTP调试日志

- - 更新flutter_xboard_sdk到最新版本
- - 移除了HttpService的详细请求/响应日志输出
- - 清理生产环境的调试信息

- 清理调试代码

- - 删除套餐限速调试时添加的print语句
- - 限速显示问题已修复，不再需要调试输出
- - 保持代码整洁

- 简化购买套餐页面UI

- - 删除套餐详情描述卡片(PlanDescriptionWidget)
- - 仅保留套餐标题、流量和限速核心信息
- - 移除多余的content展示，提升页面简洁性
- - 用户可更快速了解套餐要点并进行购买决策

- 更新SDK submodule引用

- - 更新flutter_xboard_sdk到最新版本
- - 包含Plan模型speedLimit字段JSON映射修复

- 修复套餐信息页面限速字段显示问题

- - 修复SDK Plan模型中speedLimit字段的JSON映射
- - 添加@JsonKey(name: 'speed_limit')注解正确映射API返回的speed_limit字段
- - 重新生成freezed和json_serializable代码
- - 现在套餐限速信息能正确显示实际速度值而不是始终显示unlimited

- feat: 默认开启TUN模式

- - 修改defaultTun配置，默认启用TUN模式
- - 更新main.dart中的快速启动配置，默认开启TUN
- - 确保新用户和配置重置时TUN模式默认启用

- refactor: 实现集中化提供商配置，去掉降级处理

- - 添加XBoardProviderConfig统一管理当前使用的提供商
- - 重构配置访问逻辑，支持通过常量切换提供商
- - 去掉所有降级处理逻辑，简化代码结构
- - 修改PanelConfiguration支持动态提供商选择
- - 更新XBoardConfigAccessor使用当前提供商配置
- - 简化XBoardConfigAPI接口，提供统一的入口方法
- - 更新域名提取逻辑，只提取当前提供商域名
- - 移除应用启动时的降级处理

- 切换提供商方法：
- 只需修改XBoardProviderConfig.CURRENT_PROVIDER常量
- - 'wujie' -> wujie提供商
- - 'v2word' -> v2word提供商

- feat: 添加XBoard配置访问器

- - 实现简单属性访问方式 (config.ws_url, config.proxy_url 等)
- - 支持索引访问 (getWsUrl(index: 1))
- - 支持提供商特定访问 (getPanelUrls(provider: 'wujie'))
- - 支持元数据访问 (getWsDescription, getProxyProtocol)
- - 支持批量访问 (getAllProxyInfo)
- - 集成现有RemoteConfigManager
- - 支持响应式更新 (ChangeNotifier)
- - 添加到依赖注入系统
- - 提供XBoardConfigAPI便捷访问类

- 解决命名冲突：
- - 重命名ProxyInfo为ConfigProxyInfo避免与domain_selector冲突
- - 使用精确导出避免命名空间污染

- feat: 添加域名服务测试脚本并修复域名提取逻辑

- - 添加独立的域名服务测试脚本test_domain_service.dart
- - 修复XBoardDomainProvider中的域名提取逻辑，支持新的配置格式
- - 兼容panels.wujie和panels.v2word结构
- - 测试结果显示所有功能正常：
-   * 远程配置获取：✅ 成功
-   * 域名提取：✅ 找到4个域名
-   * 连通性测试：✅ 全部通过
-   * 最佳域名选择：✅ 自动选择最低延迟
-   * 域名验证和刷新：✅ 功能正常

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 删除域名服务降级策略，没有域名就直接失败

- - 修改main.dart中的_initializeXBoardServices，删除降级逻辑
- - 修改XBoardService.initialize，没有域名时直接抛出异常
- - 修改XBoardDomainService和Facade支持接收null baseUrl
- - 简化逻辑，完全依赖域名服务，无域名就失败

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor(xboard): 完全重构domain_service为模块化架构

- 重构亮点：
- - 📦 模块化设计：拆分为7个独立的业务服务
-   - AuthService: 认证相关
-   - UserService: 用户信息管理
-   - SubscriptionService: 订阅套餐
-   - PaymentService: 支付订单
-   - SupportService: 工单系统
-   - SystemService: 系统配置
-   - InviteService: 邀请推荐

- 架构改进：
- - 🏗️ 采用接口+实现分离的设计模式
- - 🔧 统一的XBoardService核心服务管理
- - 🔄 完全向后兼容的门面模式
- - ♻️ 保留所有原有的适配器和模型代码

- 修复问题：
- - 🐛 注释域名状态相关代码避免编译错误
- - ✨ 添加静态方法支持向后兼容调用
- - 🔧 修复方法名冲突问题

- 技术优势：
- - 📈 更好的可扩展性和可测试性
- - 🎯 单一职责原则，代码更清晰
- - 🚀 保持原有API完全不变

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix(xboard): 清理domain_service中的业务逻辑引用错误

- - 移除对已删除文件的导入引用
- - 修复DomainStrategyType未定义问题，改为字符串类型
- - 简化SDK初始化逻辑，添加TODO标记
- - 注释未使用的测试环境检测方法
- - 保留适配层和封装层接口不变

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat(xboard): Ignore SSL errors and remove config demo

- fix: 回退domain_service中两个文件到稳定版本

- - 回退config_fetcher.dart到简单实现
- - 回退smart_route_domain_manager.dart到基础版本
- - 移除复杂的依赖注入引用，恢复项目可运行状态

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 重构XBoard配置模块为完全依赖注入架构

- - 移除所有静态方法和单例模式
- - 采用依赖注入容器管理组件生命周期
- - 实现工厂模式、策略模式、仓储模式
- - 提供完整的可测试性支持
- - 添加统一的配置管理类ConfigSettings
- - 创建服务定位器和DI容器
- - 重构所有核心组件支持依赖注入
- - 添加使用示例和文档

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完善域名选择器模块化架构和代理功能

- - 重构域名选择器为模块化架构：
-   - models/: 数据模型 (ProxyInfo, TestResult)
-   - services/: 核心服务 (ConnectionTester)
-   - utils/: 工具类 (ProxyUtils, ResultAnalyzer)
-   - 保持统一的 API 接口向后兼容

- - 增强代理功能支持：
-   - 支持带用户名密码的HTTP代理格式
-   - 完善代理地址解析 (支持密码中包含特殊字符)
-   - HTTP Basic Authentication 认证
-   - 详细的错误处理和诊断

- - 创建综合配置测试系统：
-   - config_demo.dart: 完整的配置获取→格式化→域名测试流程
-   - 使用真实远程配置数据进行测试
-   - 详细的连接状态分析和报告

- - 添加完整的技术文档：
-   - README.md: 包含所有模块的 API 参考
-   - 代理连接状态说明和限制
-   - 使用示例和调试指南

- - 测试验证结果：
-   - HTTP网站 + 代理: 100% 成功
-   - HTTPS网站 + 直连: 100% 成功
-   - HTTPS网站 + 代理: 受代理服务器SSL隧道限制

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 回退代理设置到简单实现

- - 移除复杂的代理认证逻辑
- - 回到之前可工作的简单代理设置
- - 保持HTTP代理的基本功能

- feat: 添加代理连通性诊断功能

- - 新增testProxyConnectivity方法测试代理服务器连通性
- - 改进代理解析错误处理，提供更详细的错误信息
- - 在demo中添加代理连通性预检测
- - 帮助诊断代理连接失败的原因

- refactor: 重构域名选择器模块化架构

- - 分离模型到src/models目录：TestResult, DomainResult, DomainTestResult, TestStatistics
- - 分离服务到src/services目录：ConnectionTester处理连接测试逻辑
- - 重构主类DomainSelector，专注于API和缓存管理
- - 重写demo展示新的API使用方式和重试功能
- - 提供完整的模块化架构，便于维护和扩展

- feat: 重构域名选择器API，支持结构化结果和重试

- - 新增DomainTestResult类返回结构化测试结果
- - 支持按域名分组的直连和代理结果
- - 添加重试API：retryAll, retrySingleCombination, retryFailedCombinations
- - 提供统计信息和最佳连接推荐
- - 支持结果缓存和更新机制

- fix: 修复代理认证问题

- - 正确解析带用户名密码的代理格式(user:pass@host:port)
- - 添加代理认证支持，使用HttpClientBasicCredentials
- - 新增ProxyInfo类存储代理信息
- - 修复407 Proxy Authentication Required错误

- perf: 调整超时时间为2秒

- - 将连接超时时间从3秒调整为2秒
- - 提高测试速度，快速识别不可用连接
- - 避免在慢速连接上浪费时间

- perf: 优化重试机制为并发模式

- - 改为并发重试而非串行重试，大幅减少测试时间
- - 使用Future.any等待第一个成功结果
- - 失败时等待所有尝试完成，选择最佳结果
- - 避免单个失败连接阻塞整体测试进度

- feat: 优化域名测试超时和重试机制

- - 调整超时时间为3秒
- - 添加3次重试机制，提高测试可靠性
- - 在测试结果中显示重试次数
- - 重试间隔100ms避免过于频繁的请求

- feat: 添加域名选择器模块

- - 新增DomainSelector类进行并发联通性测试
- - 支持直连和代理两种模式的延迟测试
- - 提供最佳连接方案推荐功能
- - 包含完整的测试结果分析和统计
- - 支持按URL和代理分组查看结果

- fix: 修复ConfigFormatter处理panels嵌套结构

- - 支持处理panels下的嵌套配置结构(panels.wujie, panels.v2word)
- - 修复getUrlsByTag方法支持点号分隔的标签名
- - 更新getAllTags方法返回所有标签包括嵌套标签
- - 现在可以正确提取panels下面的所有URL

- feat: 添加配置格式化工具和demo代码

- - 新增 ConfigFormatter 类用于清洗配置数据，只提取键和URL字段
- - 新增 ConfigDemo 类展示完整的配置获取和格式化流程
- - 优先使用重定向配置源，其他配置源作为备用
- - 提供获取指定标签URLs和所有标签的便捷方法

- feat: 添加重定向配置源支持

- - 新增 RedirectConfigSource 支持未加密的重定向域名 API
- - 重构 RemoteConfigManager 支持多配置源并发获取
- - 配置层只负责获取数据，不做决策，由调用方处理配置
- - 支持同时获取两个配置源结果，支持单独获取特定配置源
- - 添加 MultiConfigResult 封装多配置源结果
- - 更新 API 文档和使用示例

-  移动了一下文件位置

- refactor: simplify remote_config module

- - 简化 RemoteConfigManager API，只保留核心功能
- - 移除复杂的状态管理和多配置源逻辑
- - 提供简单的 getConfig() 和 refreshConfig() 接口
- - 专注于 Gitee 配置获取和 AES-GCM 解密
- - 返回纯净的配置数据，其他逻辑交给调用方处理

- feat: add remote_config module

- - 实现纯 Dart 远程配置获取模块
- - 支持 Gitee 配置源，包含 AES-GCM 解密
- - 提供单例管理器和优先级降级机制
- - 包含完整的错误处理和状态管理
- - 支持面板配置和代理配置获取

- fix: 修复支付成功后状态检查和强制刷新订阅配置

- - 恢复支付状态检查功能，使用XBoardDomainService.getOrderByTradeNo方法
- - 修正支付状态逻辑：0-等待中，3-已完成，其他-失败
- - 修复PaymentWaitingManager回调丢失问题（先保存回调再隐藏弹窗）
- - 添加强制刷新参数forceRefresh，支付成功后跳过重复URL检测
- - 增加详细调试输出，便于问题追踪
- - 支付成功后自动刷新订阅信息并返回首页

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 删掉多余的导入

- fix: 修复XBoard订单创建和支付提交流程构造函数问题

- - 完善购买服务实现，移除UnimplementedError占位符
- - 修复订单创建流程中的数据类型转换问题
- - 优化支付提交逻辑，支持重定向和成功状态处理
- - 更新域名服务接口，添加缺失的订单管理方法
- - 修复支付Provider中tradeNo提取逻辑
- - SDK层添加submitPayment接口避免构造函数问题

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 完成XBoard支付系统域名服务迁移

- ## 主要更改

- ### 1. 类型系统统一
- - 更新所有支付相关接口使用域名服务数据模型
- - 修复Plan -> PlanData, Order -> OrderData, PaymentMethodInfo -> PaymentMethodInfoData类型转换
- - 移除对flutter_xboard_sdk类型的直接依赖

- ### 2. 架构优化
- - 完善ModelAdapter以支持tags字段传递
- - 移除废弃的setAuthToken方法调用
- - 统一错误处理机制

- ### 3. 数据模型完善
- - 在SDK和Domain Service中添加tags字段支持
- - 确保数据流向正确：API -> SDK -> Adapter -> Domain
- - 保持架构分层清晰

- ### 4. 文件清理
- - 删除临时适配文档和示例文件
- - 更新SDK子模块引用

- ### 修复的文件
- - purchase_interface.dart: 统一接口类型声明
- - purchase_service_impl.dart: 实现新的数据模型转换
- - xboard_payment_provider.dart: 更新状态管理类型
- - xboard_subscription_provider.dart: 支持PlanData类型
- - plans.dart, plan_purchase_page.dart: 页面组件类型适配
- - payment_gateway_page.dart: 移除废弃认证调用
- - service_providers.dart: 简化令牌管理

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- 完善XBoard域名服务测试框架

- ✨ 新增功能:
- - 添加完整的E2E测试套件 (test/xboard_domain_service_e2e_test.dart)
- - 支持智能路由策略测试，包含真实域名初始化
- - 支持真实用户凭据登录测试 (test@gmail.com)
- - 完整的API接口测试覆盖

- 🔧 修复和改进:
- - 修复SDK适配问题，确保API调用与flutter_xboard_sdk兼容
- - 修复token存储问题，测试环境自动使用内存存储
- - 修复登录流程，正确保存和验证token状态
- - 修复模型适配器语法错误和类型转换问题
- - 优化策略名称显示，返回英文标识符

- 🧪 测试验证:
- - 智能路由策略初始化 ✅
- - 真实API调用和响应处理 ✅
- - Token管理和登录状态检查 ✅
- - 错误处理和异常捕获 ✅

- 📦 依赖更新:
- - 更新pubspec.yaml测试依赖配置

- feat: 完成Domain Service数据模型适配

- - 创建完整的ModelAdapter适配器，支持SDK到Domain模型转换
- - 建立Domain异常体系，统一异常处理机制
- - 扩展Domain Service接口，添加所有缺失的业务方法
- - 实现完整的Domain Service功能，覆盖认证、订单、工单、邀请等
- - 新增完整的数据模型：认证、订单、支付、工单、邀请、优惠券等
- - 提供业务友好的API和计算属性
- - 添加使用示例和详细文档

- 主要改进：
- - SDK层和Domain层完全解耦
- - 业务语义增强，提供格式化方法和状态判断
- - 类型安全，完整的空值处理
- - 统一的错误处理和日志记录
- - 易于测试和维护的架构设计

- refactor: 完成XBoard域名服务重构，移除SDK依赖

- - 移除对flutter_xboard_sdk的直接依赖
- - 将UserInfo替换为UserInfoData，SubscriptionInfo替换为SubscriptionData
- - 为所有域名服务数据模型添加JSON序列化支持
- - 创建独立的PlanInfo数据模型
- - 更新存储服务以使用新的数据模型
- - 修复所有类型不匹配和编译错误
- - 清理不再使用的SDK转换方法和导入

- 现在代码完全使用自己的域名服务接口，不再依赖外部SDK。
- 所有核心功能（登录、用户信息、订阅数据）都通过
- XBoardDomainService.instance 访问。

- feat: 完成XBoard域名服务Provider集成

- - 重构XBoardUserAuthNotifier，直接使用XBoardDomainService
- - 移除对IAuthService的依赖，简化架构
- - 实现完整的认证功能：登录、注册、重置密码、登出
- - 修复SDK API调用问题，适配实际的SDK结构
- - 优化忘记密码页面，简化为邮箱重置流程
- - 添加完整的错误处理和状态管理
- - 保持向后兼容性，现有UI无需修改

- 核心改进：
- ✅ Provider直接集成域名服务，无中间层
- ✅ 自动重试和域名切换机制
- ✅ Token过期自动处理
- ✅ 本地存储自动管理
- ✅ 完整的状态管理和错误处理

- refactor: remove legacy adapter and finalize domain service migration

- - Remove legacy_adapter.dart and adapters directory
- - Clean up domain_service.dart exports
- - Fix core.dart import reference for subscription_url_transformer
- - All code now uses direct XBoardDomainService.instance interface
- - Complete migration from adapter pattern to direct service interface

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: fix xboard domain_service module boundaries

- - Remove cross-boundary dependencies in enhanced_app_bar.dart
- - Export connection_test.dart through public domain_service interface
- - Fix subscription_url_helper.dart to use domain_service factory
- - Remove broken config import from shared.dart
- - Clean up example files from domain_service module

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 完成XBoard域名服务重构

- - 将分散的域名管理代码重构为统一的domain_service模块
- - 删除旧的shared/config目录下的域名管理代码(~20个文件，3000+行)
- - 迁移Provider和Widget到新模块:
-   * domain_status_provider.dart -> domain_service/src/providers/
-   * route_selector_provider.dart -> domain_service/src/providers/
-   * route_selector_widget.dart -> domain_service/src/widgets/
-   * route_selector_demo.dart -> domain_service/src/widgets/
-   * subscription_url_transformer.dart -> domain_service/src/utils/
- - 修复login_page.dart和plan_purchase_page.dart中的导入引用
- - 实现统一的SDK管理器，支持智能路由、Gitee、简单域名等策略
- - 提升代码内聚性和可维护性，为后续功能扩展奠定基础

- feat: 完成XBoard域名服务重构

- ✨ 新功能:
- - 实现完整的域名服务架构重构
- - 支持智能路由、Gitee、简单域名三种策略
- - 添加完整的错误处理和重试机制
- - 实现向后兼容的适配器层

- 🔧 技术改进:
- - 重构main.dart和application.dart使用新架构
- - 更新所有相关Provider使用新的域名服务
- - 修复ConnectionMode导入问题
- - 清理旧的配置依赖

- 📚 文档:
- - 添加完整的API文档和使用示例
- - 创建性能报告和项目完成报告
- - 提供详细的迁移指南

- 🧪 测试:
- - 完整的单元测试覆盖
- - 端到端集成测试
- - 性能基准测试

- 完成42个任务，100%完成率
- 项目已可投入生产使用

- docs: add XBoard domain service migration plan

- feat: SDKManager服务初始化

- fix: restore accidentally deleted files

- refactor(xboard): remove comments and blank lines

- feat: remove comment lines

- feat: 完成XBoard域名服务重构并解决编译错误

- - 将shared/config架构完全迁移到统一的domain_service接口
- - 简化初始化流程，使用XBoardDomainService.instance统一入口
- - 修复所有编译错误，确保应用可以正常构建
- - 重构异常处理机制，简化错误管理
- - 更新所有服务实现以使用新的域名服务架构
- - 添加向后兼容适配器确保平滑迁移
- - 优化SDKManager和相关组件的错误处理

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成XBoard域名服务重构

- - 重构域名服务架构，采用三层架构设计
- - 新增domain_service模块，提供统一的域名管理接口
- - 修复所有编译错误和类型安全问题
- - 优化配置提供者和依赖注入
- - 完善测试覆盖和文档
- - 保持向后兼容性

- feat: 添加线路选择器到登录页面左上角

- ## 核心功能
- - 在登录页面左上角添加线路选择器Widget
- - 用户可手动选择网络线路或启用智能自动选择
- - 实时显示所有可用线路的延迟和连接状态

- ## 用户界面
- - 📍 位置：登录页面AppBar左上角
- - 🎨 设计：根据连接质量显示不同颜色图标
- - 📱 交互：点击显示线路下拉菜单
- - 🔄 模式：支持智能选择和手动选择切换

- ## 功能特性
- - 实时线路监控：显示延迟、可用性、成功率
- - 智能/手动模式：默认智能选择，可手动切换
- - 颜色编码指示：绿色(快速) 橙色(中等) 红色(慢速)
- - 连接模式显示：直连⚡ 代理🔒 图标标识
- - 故障自动切换：结合故障检测机制

- ## 线路信息
- 每个线路显示：
- - 线路名称和描述
- - 实时延迟(ms)和颜色编码
- - 连接模式(直连/代理)
- - 可用状态指示器

- ## 组件结构
- - RouteSelectorWidget: 主要UI组件
- - RouteSelectorProvider: 状态管理和业务逻辑
- - EnhancedAppBar: 增强版AppBar集成
- - RouteInfo/RouteSelectorState: 数据模型

- ## 用户体验
- - 默认启用智能选择模式
- - 一键切换到任意可用线路
- - 实时状态更新和故障恢复
- - 完全无感知的线路切换

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现被动故障检测和自动域名切换机制

- ## 核心功能
- - 添加 FailureDetector 智能识别网络连接故障
- - 实现 SDKFailureHandler SDK级别自动故障切换
- - 创建 ResilientHttpClient 弹性HTTP客户端
- - 集成故障检测到认证和购买服务

- ## 故障检测特性
- - 被动检测：仅在HTTP请求失败时触发
- - 智能识别：区分网络故障和业务错误
- - 快速恢复：立即切换无需等待缓存过期
- - 用户透明：故障切换完全无感知
- - 防护机制：1分钟冷却期防止系统抖动

- ## 故障切换流程
- 1. HTTP请求失败 → 故障检测器识别连接故障
- 2. 清除缓存 → 智能路由重新选择最优域名
- 3. SDK重初始化 → 使用新域名重新初始化
- 4. 自动重试 → 透明恢复用户操作

- ## 技术实现
- - 支持 SocketException, HttpException, TimeoutException
- - 最大重试2次，递增延迟机制
- - 冷却期1分钟，并发保护
- - 完整的日志记录和监控

- ## 服务集成
- - 认证服务：登录、注册等操作自动故障切换
- - 购买服务：套餐、订单、支付等操作自动故障切换
- - 解密优化：统一使用16字节nonce格式

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现纯智能路由架构并修复解密问题

- ## 核心架构变更
- - 实现纯智能路由架构，移除所有兜底机制
- - 智能路由返回两个值：域名和连接模式(direct/proxy)
- - 创建 ConnectionConfig 和 ConnectionMode 数据结构
- - 新增 SmartRouteDomainManager 实现纯路由逻辑

- ## 主要修改
- - 重构 domain_manager_interface.dart 添加新接口
- - 创建完整的智能路由模块 smart_route_domain_manager/
- - 更新 XBoardConfig 移除fallback相关字段
- - 修复 main.dart 中的provider引用冲突

- ## 解密问题修复
- - 修复 GiteeDomainService 解密失败问题
- - 添加详细调试日志和16字节nonce备用方案
- - 统一解密逻辑，处理不同nonce长度格式

- ## 兼容性保持
- - 创建 compatibility.dart 提供向后兼容
- - 保留deprecated方法确保平滑迁移
- - 更新所有相关服务使用新架构

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- chore: 更新依赖锁定文件

- - 更新pubspec.lock和Podfile.lock以反映新增的依赖项

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现双策略域名管理架构和Gitee域名管理器

- - 新增Gitee域名管理器，支持从Gitee获取动态域名配置
- - 重构域名提供者架构，支持主策略(Gitee)和备用策略(Redirect)的fallback机制
- - 更新动态域名配置管理器，支持双策略验证和缓存管理
- - 优化域名状态提供者，使用新的fallback机制
- - 添加加密和HTTP依赖以支持域名获取功能

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 集成XBoard SDK代理支持到主应用

- - 更新XBoardConfig添加proxyUrl字段
- - 修改XBoardSDKManager支持代理配置传递
- - 在config_provider中配置默认代理地址
- - 更新SDK子模块到最新版本

- 这允许XBoard所有HTTP请求通过指定的代理服务器

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: XBoard 模块目录结构重构

- 🏗️ 重构概述
- - 采用基于功能领域的目录组织方式
- - 将原有分散的目录结构重构为 features（功能模块）和 shared（共享组件）架构
- - 提高代码的可维护性、可扩展性和模块化程度

- 📁 新目录结构
- - features/auth/          # 认证功能（登录、注册、密码重置）
- - features/payment/       # 支付功能（套餐购买、支付处理）
- - features/subscription/  # 订阅功能（订阅管理、使用量显示）
- - features/profile/       # 配置导入功能
- - features/system/        # 系统功能（延迟检测、远程任务、更新检查）
- - shared/config/          # 配置管理
- - shared/models/          # 数据模型
- - shared/providers/       # 共享状态管理
- - shared/services/        # 共享服务
- - shared/utils/           # 工具类
- - shared/widgets/         # 通用UI组件

- ✨ 主要改进
- - ✅ 模块化架构：按功能领域组织代码
- - ✅ 清晰的职责分离：Features 处理具体功能，Shared 提供通用组件
- - ✅ 向后兼容性：保持现有导入接口不变
- - ✅ 统一的导出文件：每个模块都有清晰的导出接口
- - ✅ 完整的文档：提供详细的使用和维护指南

- 🔧 技术改进
- - 修复了所有导入路径问题
- - 更新了 Provider 引用
- - 创建了模块化的导出文件
- - 添加了完整的 README 文档

- 📊 验证结果
- - ✅ 编译验证通过
- - ✅ 所有 XBoard 功能保持完整
- - ✅ 状态管理系统运行正常

- feat: Refine plan content display and revert speed limit changes

- feat: Enhance payment process and user experience

- fix(xboard): 修复支付网关URL解析和标准响应格式处理

- - 更新SDK子模块到最新版本，支持标准响应格式
- - 修复支付数据解析逻辑，正确处理HttpService包装后的数据结构
- - 更新purchase_service_impl恢复标准ApiResponse处理
- - 优化支付URL提取逻辑，支持{type:1, data:"url"}格式
- - 确保支付链接能正确在外部浏览器中打开

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix(xboard): 修复支付提交API参数格式和状态检查错误

- - 修正PaymentRequest字段映射，tradeNo -> trade_no
- - 修复支付状态检查API返回类型转换错误
- - 完善支付结果处理，支持嵌套数据结构
- - 优化支付URL提取和浏览器启动逻辑
- - 正确映射订单状态码: 0=等待中, 2=已取消, 3=支付成功

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix(xboard): 修复SDK集成后的多处编译错误

- - 统一UserAuthState模型，包含userInfo和subscriptionInfo
- - 修正plan_purchase_page.dart中paymentProvider的错误用法，改为监听userUIStateProvider
- - 调整xboard_home_page.dart中订阅信息和用户信息获取方式，直接从ref获取
- - 修复xboard_payment_provider.dart中Notifier类型为void导致的问题
- - 修复xboard_subscription_provider.dart中Notifier类型为List<Plan>导致的问题
- - 更新相关接口和实现，以适应SDK数据结构和token管理方式

- refactor(xboard): 完善 SDK 集成和 token 管理

- - 修复用户信息解析错误，支持 telegram_id 的 int/string 转换
- - 完善登录后的 provider 数据更新流程
- - 标记 storage_service 中的 token 方法为已弃用，token 管理完全由 SDK 负责
- - 优化 XBoardSDKManager 的初始化和错误处理
- - 改进 auth_service_impl 中的 SDK 集成逻辑

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor(xboard): 重构数据结构直接使用SDK，移除数据转换层

- - 移除XBoardUserState中的authToken字段，token管理完全交给SDK
- - 直接使用SDK的UserInfo和SubscriptionInfo数据结构
- - 更新认证服务实现，完全委托给SDK的TokenManager
- - 更新所有providers移除authToken依赖和setAuthToken调用
- - 简化架构，减少数据同步问题，提高维护性

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: SDK initialization and login display fix

- feat(xboard): Update SDK submodule with improved notice API handling

- - Update flutter_xboard_sdk submodule to latest commit (803202f)
- - SDK improvements include better error handling and response validation
- - Enhanced notice API with ApiResponse wrapper for standardized responses
- - Remove unused documentation files from SDK

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat(sdk): Modularize auth and config features, refactor models with freezed/json_serializable, and add integration tests

- fix: 修复重复测速问题 - 订阅重复导入导致的组件重建

- 问题根因：
- - 订阅状态检查器每次都重新获取和导入配置
- - 相同URL被重复导入触发 groupsProvider 变化
- - 组件监听器检测到变化后重复触发自动测速

- 修复方案：
- - SubscriptionStatusChecker 添加防重复机制（30秒窗口）
- - ProfileImportProvider 增强防重复导入（2分钟相同URL）
- - ImportState 添加 lastSuccessTime 字段跟踪导入时间
- - 修复 const 构造函数与非 final 字段的编译错误

- 技术实现：
- - 添加 _isChecking 标志防止并发检查
- - 记录 _lastCheckTime 实现时间防重复
- - 新增 lastSuccessTime 字段精确跟踪成功导入时间
- - 检查相同URL和时间窗口避免重复导入
- - finally 块确保状态正确重置

- 性能提升：
- - 消除重复的订阅状态检查和配置导入
- - 减少不必要的组件重建和状态变化
- - 避免自动测速的重复触发
- - 提升登录后的页面响应速度

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复支付页面token过期问题

- 问题现象：
- - 支付方式API调用返回403错误"未登录或登陆已过期"
- - 用户无法完成支付流程

- 修复内容：
- - 添加 _validateAndRefreshToken() 方法验证token有效性
- - 实现 _isAuthenticationError() 识别认证错误
- - 优化 loadPaymentMethods(), createOrder(), submitPayment() 方法
- - 在所有支付操作前进行token验证
- - 改进错误处理，提供友好的用户提示

- 技术改进：
- - 支付流程中主动验证token状态
- - 区分认证错误和其他业务错误
- - 统一的认证错误处理逻辑
- - 更清晰的错误信息反馈

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 优化登录流程和自动测速，减少重复渲染和API调用

- 主要优化内容：
- - 路由缓存：_AppHomeRouter 添加状态缓存，避免重复渲染
- - 通知优化：移除 NoticeProvider 的 autoDispose，添加缓存机制
- - 域名缓存：DynamicDomainConfigManager 添加5分钟缓存
- - 测速优化：AutoLatencyService 实现每代理独立缓存和防重复触发
- - 初始化防护：添加标志防止重复初始化和测试

- 性能提升：
- - 消除重复日志输出和API调用
- - 减少不必要的Widget重建
- - 提升登录后页面响应速度
- - 优化内存使用和电池消耗

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: Optimize login process by deferring profile loading

- feat(remote_task): 增强 WebSocket 的稳定性和消息处理

- 本次提交包含对远程任务模块的三项关键改进：

- 1.  **修复：** 对 `StatusReportingService` 进行了重构，彻底解决了 WebSocket 在连接失败或意外断开时，因未处理的异常而导致应用崩溃的问题。新的实现确保了在任何情况下都能进行稳定、可靠的自动重连。

- 2.  **完善：** 在 `RemoteTaskManager` 中增加了对服务端 `pong`（心跳响应）消息的正确处理。这避免了之前版本中将心跳响应误判为格式错误的指令，从而引发不必要错误日志的问题。

- 3.  **文档：** 更新了 `REMOTE_TASK_MODULE.md`，使其与最新的代码逻辑和消息格式保持完全同步。

- 这些改动共同提升了远程任务功能的健壮性和可靠性。

- feat: 实现客户端心跳机制

- 为防止服务端心跳超时，在 status_reporting_service.dart 中添加了定时器，每 30 秒自动发送 ping 事件。同时更新了模块文档以反映此变更。

- feat: 实现动态 nodeId 并优化 IP 获取机制

- 客户端现在会生成并持久化唯一的 nodeId，并通过 WebSocket 上报。移除了客户端主动获取公网 IP 的逻辑，改为由服务端下发 http_task 指令来灵活控制，并同步更新了文档。

- docs: 清理过时的 XBoard 文档

- feat: 实现远程任务模块

- fix(xboard): 修复注册按钮显示异常的问题

- feat(xboard): 登录页增加域名服务状态检查

- - 在登录页右上角增加服务状态指示灯和文本描述。
- - 状态包括：检查中、服务可用、服务不可用。
- - 每次进入登录页时会自动检查服务状态。
- - 当服务不可用时，会自动在后台进行周期性重试，并在网络恢复后自动更新UI状态。
- - 登录按钮只有在服务可用时才可点击。
- - 为新的UI文本添加了国际化支持。

- feat: 同步国际化翻译文件并更新工作流程文档

- - 以中文简体(intl_zh_CN.arb)为基准同步所有语言翻译文件
- - 添加缺失的订阅状态相关翻译键值到所有语言
- - 修正中文繁体翻译使用正确的繁体字符
- - 更新国际化工作流程文档使用intl_utils命令
- - 添加intl_utils依赖并自动生成所有消息文件

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复登录成功后不跳转主页面的问题

- - 登录成功后使用Navigator强制导航到根路由
- - 添加_AppHomeRouter状态变化的调试日志
- - 增加LOGIN_FLOW_ANALYSIS.md详细分析登录流程
- - 解决状态更新与路由响应时机不匹配的问题

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 优化通知栏组件，消除加载时的闪烁效果

- - 移除加载时显示的"加载通知中..."容器
- - 加载中和无通知时都直接隐藏组件
- - 避免启动时通知栏的闪烁问题，提升用户体验

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 优化套餐页面显示效果

- - 移除套餐特性描述中的小字说明，界面更简洁
- - 去掉"套餐特色"标题，直接显示特性列表
- - 智能判断限速显示：无限速相关描述时显示"Unlimited"
- - 简化PlanDescriptionWidget组件，去掉冗余代码
- - 优化套餐卡片布局，提升用户体验

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复登录成功后不跳转主页面的问题

- - 在登录成功后添加延迟和状态刷新确保页面跳转
- - 解决Riverpod状态监听延迟导致的_AppHomeRouter响应问题
- - 修复登录失败后重新登录时的状态同步问题

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复套餐卡片中"流量"和"限速"字样的国际化

- - 在plans.dart中将硬编码的"流量"替换为AppLocalizations.of(context).xboardTraffic
- - 在plans.dart中将硬编码的"限速"替换为AppLocalizations.of(context).xboardSpeedLimit
- - 添加必要的国际化导入

- 现在套餐卡片中的"流量"和"限速"标签会根据用户语言设置正确显示

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成套餐状态提示语的国际化支持

- - 在ARB文件中添加套餐状态相关的国际化字符串
- - 重构SubscriptionStatusResult类支持动态国际化
- - 修复所有相关组件使用国际化字符串替代硬编码中文
- - 更新subscription_status_service使用函数回调获取国际化文本
- - 修复subscription_usage_card、subscription_status_dialog等组件的国际化调用

- 现在套餐过期、流量用完等提示会根据用户语言设置正确显示

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成启动代理按钮的国际化

- - 添加启动/停止代理按钮的多语言文本
- - 添加运行时间显示的国际化支持
- - 支持参数化的国际化文本(运行时间)
- - 更新所有4种语言的国际化文件和messages文件
- - 修复XBoard连接按钮硬编码的中文文本

- 新增国际化键:
- - xboardStartProxy: 启动代理按钮文本
- - xboardStopProxy: 停止代理按钮文本
- - xboardRunningTime: 运行时间显示文本(带参数)

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复l10n文件中重复的xboardHandleLater定义

- - 删除重复的国际化键定义
- - 修复编译错误
- - 确保所有新增的国际化键不与现有键冲突

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成XBoard模块剩余部分的国际化

- - 添加代理模式卡片的国际化文本
- - 添加无可用节点卡片的国际化文本
- - 添加订阅状态弹窗的国际化文本
- - 修复context访问问题
- - 更新所有语言的国际化文件(英语、中文、日语、俄语)
- - 支持多语言显示：代理模式描述、节点管理、订阅状态提示等

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加XBoard完整国际化支持和用户体验优化

- - 新增完整的XBoard模块多语言支持（英语、日语、俄语、中文）
- - 优化登录、注册、订阅购买等页面的用户体验
- - 增强支付流程的状态提示和错误处理
- - 改进订阅使用状态展示和交互逻辑
- - 统一多语言文案风格和术语表达

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- chore: 更新flutter_xboard_sdk子模块到最新版本

- - 引用最新的订阅模型扩展功能

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加XBoard订阅状态检查和用户体验优化

- - 新增订阅状态检查服务，自动检测订阅过期、流量用完等状态
- - 优化订阅使用量卡片组件，简化代码逻辑并改善用户界面
- - 添加订阅状态对话框，提醒用户续费或购买更多流量
- - 更新重定向域名服务的源参数为v2word.one
- - 在首页启动时集成订阅状态检查功能
- - 更新SDK子模块和导出文件

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 修改应用名称为「无界畅游」并修复HTTP头错误

- - 所有平台应用名称改为「无界畅游」
- - 添加英文名称 WujieChangyou 用于HTTP User-Agent
- - 修复中文字符在HTTP头中导致的格式错误
- - 保持网络请求兼容性和协议规范

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 设置默认邀请码且不可更改，更新版本号

- - 注册页面邀请码默认设为 lc6WRbRg
- - 邀请码输入框设为禁用状态，用户不可修改
- - 更新版本号为 2.5.9+2025072901

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 更新初次启动提示框为公测阶段通知

- - 修改标题从"免责声明"为"重要提示"
- - 更新内容为公测阶段提醒和更新提示
- - 支持多语言版本（中英日俄）
- - 提醒用户及时更新避免服务不稳定

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 重新设计登录、注册和忘记密码页面，增加记住密码功能

- 主要更新：
- - 采用一体化背景设计，移除卡片样式
- - 使用自定义XB组件（XBInputField、XBCard、XBContainer）
- - 添加记住密码功能，支持凭据自动填充
- - 注册成功后自动返回登录页面并填充账号密码
- - 优化UI布局，支持响应式设计
- - 添加密码可见性切换功能
- - 移除注册页面的邮箱验证码要求
- - 修复认证服务对空邮箱验证码的处理
- - 改进错误处理和用户反馈

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加TUN模式首次使用介绍弹窗

- - 创建TunIntroductionDialog组件，精美介绍TUN模式特性
- - 扩展XBoardStorageService支持首次使用状态存储
- - 添加推荐使用方式：规则+TUN（日常）、全局+TUN（备用）
- - 集成智能弹窗逻辑：首次点击显示介绍，后续直接切换
- - 用户可选择立即开启或稍后再说，避免强制打扰
- - 使用Material Design 3设计规范，绿色盾牌主题

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 将代理模式直连按钮替换为TUN模式开关

- - 创建XBoardOutboundMode组件，保持原有卡片设计风格
- - 规则/全局模式保持互斥选择逻辑
- - TUN开关独立于代理模式，可与规则/全局共存
- - 保留全局模式自动节点选择和测速功能
- - 使用绿色主题区分TUN开启/关闭状态
- - 状态描述动态显示TUN启用状态

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 更新XBoard页面和providers以使用新的动态域名服务

- - 更新所有页面以使用新的service providers
- - 移除旧的静态auth_service和purchase_service文件
- - 更新provider导入路径以匹配新的架构
- - 完善storage_service集成

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复XBoard动态域名解析时序问题

- - 修复DynamicDomainConfigManager在loading状态下立即返回兜底域名的问题
- - 服务初始化现在会等待动态域名解析完成，避免使用兜底域名进行API请求
- - 为动态域名解析添加超时保护机制，防止无限等待
- - 完善动态域名系统的错误处理和日志记录
- - 集成动态域名系统到auth_service_impl和purchase_service_impl
- - 移除旧的静态服务实现，统一使用动态域名架构

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现XBoard动态域名管理系统

- - 新增动态域名管理模块，支持自动获取和缓存最佳可用域名
- - 实现RedirectDomainManager重定向域名管理器，支持6小时缓存
- - 新增domain providers用于Riverpod状态管理
- - 扩展XBoardConfig支持动态域名配置选项
- - 优化config_provider支持动态域名获取
- - 完全集成现有xboard框架，使用统一日志和错误处理
- - 支持手动刷新域名缓存和后台验证域名有效性

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: 简化XBoard配置系统为统一入口

- - 移除环境区分逻辑(development/staging/production)
- - 统一API URL管理，避免硬编码
- - 所有服务通过配置注入获取API地址
- - 简化配置Provider和管理类

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现重新登录弹窗跳转到登录页面功能

- - 在token过期弹窗中添加登录页面导航功能
- - 使用pushAndRemoveUntil清除所有页面栈，确保用户无法返回到过期状态页面
- - 优化用户重新认证体验

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复支付成功后订阅刷新问题

- - 修复Widget销毁导致刷新被跳过的问题，先执行刷新再导航
- - 完善refreshSubscriptionInfo方法，在获取新订阅信息后重新导入配置
- - 添加详细的日志跟踪支付成功和刷新流程
- - 确保支付成功后能正确更新订阅状态和重新导入配置文件

- 修复流程：
- 1. 检测到支付成功，显示成功状态
- 2. 用户确认或3秒后，先执行订阅刷新操作
- 3. 延迟300ms后导航回首页，确保刷新已开始
- 4. 刷新过程中重新导入订阅配置到主应用

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现支付等待覆盖页面和自动状态检测

- - 新增PaymentWaitingOverlay组件，提供完整的支付流程等待体验
- - 支持四个支付步骤：创建订单、加载支付页面、验证支付方式、等待支付完成
- - 实现每5秒自动检测支付状态功能，使用/api/v1/user/order/check接口
- - 支付成功时在弹窗中显示成功状态，3秒后自动关闭或手动确认
- - 采用原项目AlertDialog风格，适配主题色彩系统
- - 优化用户体验：动画效果、状态反馈、错误处理

- 主要特性：
- - 全屏等待遮罩，阻止用户其他操作
- - 步骤式进度指示，让用户了解当前状态
- - 自动支付状态轮询，无需手动刷新
- - 支付成功后优雅的确认界面
- - 完善的错误处理和异常恢复

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完成支付流程优化和SDK架构重构

- - 简化支付流程：删除中间支付页面，直接在浏览器打开支付链接
- - 修复SDK认证问题：统一所有服务使用HttpService
- - 优化支付响应解析：支持type+data格式的重定向
- - 更新SDK子模块到最新版本

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加余额抵扣提示功能

- 主要改进:
- - 添加账户余额显示功能，页面初始化时自动加载
- - 在购买按钮上方显示简洁的余额提示
- - 有余额时显示"支付时可抵扣"绿色标签
- - 无余额时以灰色样式显示余额信息
- - 修复SDK中余额获取方法调用错误
- - 采用非侵入式设计，不影响现有购买流程

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 优化购买套餐页面UI和优惠券验证功能

- 主要改进:
- - 移除套餐content内容显示，界面更简洁
- - 移除待支付订单显示功能
- - 修复流量显示计算错误(transferEnable已为GB单位)
- - 购买周期默认选择第一个可用选项
- - 美化优惠券输入框样式，添加状态指示
- - 实现优惠券核验功能，支持金额和百分比折扣
- - 添加原价划线显示，突出优惠效果
- - 修复SDK中CouponData模型的limitPlanIds字段类型

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 美化套餐页面展示效果

- - 修复流量显示为0GB的问题，正确显示套餐流量信息
- - 创建PlanDescriptionWidget美化套餐详细介绍，支持智能识别特性类型并分配图标和颜色
- - 优化套餐卡片设计，价格显示在右上角，移除详细价格选项栏
- - 实现响应式布局：桌面端使用固定宽度(350px)的网格布局，手机端保持列表布局
- - 桌面端隐藏AppBar以增加显示空间，手机端保持标题栏
- - 支持流量、带宽、优惠券、流媒体解锁等特性的可视化展示

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 修复全局模式默认选择DIRECT节点问题

- - 添加模式切换处理逻辑，在切换到全局模式时自动选择有效代理节点
- - 过滤DIRECT和REJECT节点，优先选择真正的代理节点
- - 优化日志输出，减少调试信息的噪音

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- update: 修复自动登录token

- fix: 修复UserInfo模型中bool字段类型转换错误

- - 修改SDK中banned、remind_expire、remind_traffic字段解析逻辑，支持服务器返回的bool类型
- - 添加token验证前的日志输出用于调试
- - 添加详细的错误处理和调试信息

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加应用版本更新检查功能和公告板HTML支持

- 版本更新功能:
- - 新增完整的版本更新检查系统
- - 应用启动时自动检查更新
- - 支持手动检查更新(关于页面)
- - 精美的更新弹窗，支持强制更新
- - 完善的错误处理和用户反馈
- - 使用GET请求适配实际API接口

- 公告板HTML支持:
- - 通知横幅支持HTML格式渲染
- - 通知详情弹窗支持完整HTML/CSS
- - 支持常见HTML标签(h1-h6, p, strong, em, ul, ol, a等)
- - 自动适配主题颜色和字体大小
- - 保持原有滑动切换动画效果

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加通知横幅功能，支持上下滑动切换和详情弹窗

- - 新增NoticeBanner组件，支持上下滑动切换通知标题
- - 新增NoticeProvider状态管理，处理通知数据获取和过滤
- - 新增NoticeDetailDialog弹窗，支持查看完整通知内容
- - 集成到XBoardHomePage顶部显示
- - 支持点击查看详情，多条通知自动切换
- - 只显示带app标签且shouldShow=true的通知

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修复代理页面Material上下文错误

- - 使用CommonScaffold包装ProxiesView解决Material上下文问题
- - 修复TabBar在Navigator.push时缺少Material上下文的错误
- - 保持页面标题为"代理"提供更好的用户体验

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 修改代理切换为直接打开页面而非页面切换

- - 将NodeSelectorBar中的所有代理切换按钮改为使用Navigator.push
- - 避免页面切换动画和闪现其他页面的问题
- - 直接打开独立的ProxiesView页面，提供更好的用户体验

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 隐藏手机端底部导航栏

- - 移除手机端底部导航栏显示
- - 保持桌面端侧边导航栏不变
- - 简化手机端界面，专注于主要功能

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 将登录成功后的默认主页面改为xboard页面

- - 修改AppState中默认pageLabel从dashboard改为xboard
- - 用户登录成功后直接进入XBoard主页面
- - 重新生成Freezed代码以应用更改

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 桌面端隐藏xboard页面右上角plans按钮

- - 桌面端通过侧边导航栏访问plans页面
- - 移动端保持右上角显示plans按钮
- - 使用system.isDesktop判断平台差异

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 在xboard页面右上角添加套餐信息入口

- - 修复双AppBar问题，使用PageMixin正确管理页面状态
- - 在右上角导航栏添加礼品卡图标按钮，点击跳转到套餐信息页面
- - 移除重复的Scaffold包装，使用父级CommonScaffold统一管理
- - 更新API入口地址为wujie05.wujie001.art

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- update: 更新入口地址

- feat: 实现节点切换自动延迟测试功能

- - 优化AutoLatencyService，支持智能等待配置导入完成
- - 新增节点切换时自动触发延迟测试机制
- - 监听代理组和配置文件变化，自动启动延迟测试
- - 改进服务生命周期管理和错误处理
- - 移除节点卡片中多余的连接状态显示
- - 将手动测试提示改为"自动测试中"

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- cleanup: 删除未使用的xboard_user_provider_v2.dart

- - 删除实验性的v2版本provider
- - 保留正在使用的xboard_user_provider.dart作为主版本
- - 清理冗余代码，简化项目结构

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 实现订阅链接转换功能和修复AutoLatencyService生命周期问题

- - 添加订阅链接转换工具，支持模块化扩展
- - 原始格式转API格式：/s/token -> /api/v1/subscription/token
- - 集成到profile_import_provider中自动转换订阅链接
- - 修复AutoLatencyService中ref生命周期问题
- - 添加ref有效性检查，防止disposed异常

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- fix: 解决XBoard组件编译错误和延迟测试集成

- - 修复NodeSelectorBar中缺失的testUrl属性引用
- - 添加LatencyIndicator组件并修复空值处理
- - 修复AutoLatencyService中缺失的枚举类型引用
- - 修复Flutter图标常量名称错误
- - 完善XBoard页面与延迟测试服务的集成

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 完善NodeSelectorBar组件实现真实节点显示

- - 修复URLTest组节点显示逻辑，现在能正确显示Go后端自动选择的具体节点名称
- - 实现Selector组到URLTest组的引用跟踪机制
- - 重构节点选择逻辑，直接集成原项目的groupsProvider和selectedMapProvider
- - 移除自定义NodeInfo和NodeSelectorState模型，改用原生Proxy类
- - 优化Rule模式下的组选择算法，正确处理组间引用关系
- - 清理未使用的provider和dialog组件，简化代码架构

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: 添加节点选择器横条功能

- - 实现 NodeSelectorBar 组件显示当前节点信息
- - 添加节点切换功能和选择对话框
- - 集成原项目代理切换机制
- - 支持状态指示器和实时更新
- - 在仪表板页面中集成组件进行测试

- feat: 缓存式登录优化，启动时直接进主界面，后台验证token有效性，失效弹窗提示

- 优化xboard主页布局和配置导入体验

- - 重新排列主页组件顺序：订阅用量→代理模式→当前节点→启动代理
- - 移除独立的代理状态提示卡片，简化界面
- - 将配置导入进度功能整合到订阅用量卡片中，提升空间利用率
- - 实现导入成功状态的自动隐藏机制(2秒后自动消失)
- - 修复所有弃用的withOpacity方法调用
- - 移除不再需要的订阅信息和快捷操作部分

- feat: 实现XBoard稳定配置导入系统

- ✨ 新增功能:
- - 添加专用的配置导入服务，支持重试机制和错误处理
- - 实现导入状态管理，提供实时进度反馈
- - 创建用户友好的导入进度显示组件
- - 集成到XBoard主页，替换原有不稳定的导入方法

- 🔧 技术改进:
- - 每次导入前自动清理旧配置，解决配置累积问题
- - 30秒下载超时 + 3次重试机制，提升网络稳定性
- - 操作锁定防止重复导入，避免竞争条件
- - 详细的错误分类和用户友好提示

- 📁 新增文件:
- - lib/xboard/models/import_models.dart - 导入相关数据模型
- - lib/xboard/services/profile_import_service.dart - 稳定导入服务
- - lib/xboard/providers/profile_import_provider.dart - 导入状态管理
- - lib/xboard/widgets/profile_import_progress.dart - 进度显示组件

- 🔄 修改文件:
- - 更新用户provider使用新的导入服务
- - 集成进度组件到XBoard主页
- - 改进手动导入按钮反馈

- feat: 添加XBoard独立首页模块

- - 新增XBoard首页 (xboard_home_page.dart) 集成一键连接、节点信息、订阅信息和代理模式
- - 新增独立连接按钮组件 (xboard_connect_button.dart) 支持内嵌和浮动两种模式
- - 优化页面布局：连接按钮内嵌到页面内容中，移除浮动按钮
- - 保持模块独立性：复制原项目功能逻辑但不直接依赖原项目组件
- - 新增导航支持：在主应用中添加XBoard页面入口
- - 完善文档：添加详细的使用说明和架构文档

- 主要特性：
- - 🔗 一键连接控制（内嵌式大按钮设计）
- - 📡 当前节点信息展示
- - 📋 订阅信息管理和刷新
- - ⚙️ 代理模式切换
- - 🚀 快捷操作面板
- - �� 响应式设计，适配不同屏幕

- refactor(xboard): introduce service abstraction and error handling

- fix(xboard): 修复用户登录状态在页面切换时丢失的问题

- - 将 XBoardUserNotifier 从 AutoDisposeNotifier 改为 Notifier
- - 将 XBoardSubscriptionNotifier 从 AutoDisposeNotifier 改为 Notifier
- - 将 XBoardPaymentNotifier 从 AutoDisposeNotifier 改为 Notifier
- - 确保用户登录状态在应用生命周期中保持
- - 解决登录后进入 plans 页面提示'请先登录'的问题

- 修复前: AutoDispose 机制在页面切换时自动清除状态
- 修复后: 状态在整个应用使用过程中保持，直到主动登出

- refactor(xboard): 模块化重构优化

- 🔧 主要改进:
- - 拆分大文件: plan_purchase_page.dart (1633行 → 3个独立文件)
-   - plan_purchase_page.dart (638行) - 套餐购买页面
-   - payment_page.dart (440行) - 支付页面
-   - payment_gateway_page.dart (569行) - 支付网关页面

- 📦 新增统一导出:
- - pages/pages.dart - 统一导出所有页面组件
- - services/services.dart - 统一导出所有服务

- 🎯 主入口优化:
- - xboard.dart 通过子模块统一导出
- - 保持向后兼容性，外部引用无需修改

- ✅ 验证完成:
- - 功能测试通过，所有原有功能保持不变
- - Flutter analyze 检查通过
- - 提升代码可维护性和扩展性

- feat(xboard): 增强购买和支付流程

- - 在购买页面增加待支付订单检查和显示
- - 增加批量取消待支付订单功能
- - 完善支付页面的支付方式选择器
- - 新增支付网关页面，支持外部浏览器支付
- - 增加自动轮询检测支付状态功能
- - 优化UI交互和用户体验
- - 增强错误处理和状态反馈

- Initial commit for FlClash project

- feat: add flutter_xboard_sdk as submodule

- feat: Add comprehensive plan purchase functionality

- - Create modular purchase service with SDK integration
- - Add plan purchase page with period selection and coupon support
- - Implement payment flow with order creation and submission
- - Add purchase buttons to plans page for seamless UX
- - Fix subscription import logic to replace existing subscriptions
- - Update development log with detailed implementation notes

- Features:
- - Multiple payment periods (monthly, quarterly, yearly, etc.)
- - Coupon code support for discounts
- - Integrated payment processing
- - Error handling and user feedback
- - Modular and maintainable code structure

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- refactor: Move plans page to xboard directory structure

- - Move lib/views/plans.dart to lib/xboard/pages/plans.dart
- - Update import paths in navigation.dart
- - Remove plans export from views.dart
- - Add development log for xboard changes
- - Establish xboard directory for future XBoard-related development

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: Add subscription plans page and authentication enhancements

- - Add new subscription plans view and page
- - Update authentication service with new functionality
- - Update Android build configuration
- - Update application navigation and views

- 🤖 Generated with [Claude Code](https://claude.ai/code)

- Co-Authored-By: Claude <noreply@anthropic.com>

- feat: Add authentication and subscription import feature

- Update changelog

- Fix windows tun issues

- Optimize android get system dns

- Optimize more details

- Update changelog

- Support override script

- Support proxies search

- Support svg display

- Optimize config persistence

- Add some scenes auto close connections

- Update core

- Optimize more details

- Fix issues that TUN repeat failed to open.

- Update changelog

- Fix windows service verify issues

- Update changelog

- Add windows server mode start process verify

- Add linux deb dependencies

- Add backup recovery strategy select

- Support custom text scaling

- Optimize the display of different text scale

- Optimize windows setup experience

- Optimize startTun performance

- Optimize android tv experience

- Optimize default option

- Optimize computed text size

- Optimize hyperOS freeform window

- Add developer mode

- Update core

- Optimize more details

- Add issues template

- Update changelog

- Optimize android vpn performance

- Add custom primary color and color scheme

- Add linux nad windows arm release

- Optimize requests and logs page

- Fix map input page delete issues

- Update changelog

- Add rule override

- Update core

- Optimize more details

- Update changelog

- Optimize dashboard performance

- Fix some issues

- Fix unselected proxy group delay issues

- Fix asn url issues

- Update changelog

- Fix tab delay view issues

- Fix tray action issues

- Fix get profile redirect client ua issues

- Fix proxy card delay view issues

- Add Russian, Japanese adaptation

- Fix some issues

- Update changelog

- Fix list form input view issues

- Fix traffic view issues

- Update changelog

- Optimize performance

- Update core

- Optimize core stability

- Fix linux tun authority check error

- Fix some issues

- Fix scroll physics error

- Update changelog

- Add windows storage corruption detection

- Fix core crash caused by windows resource manager restart

- Optimize logs, requests, access to pages

- Fix macos bypass domain issues

- Update changelog

- Fix some issues

- Update changelog

- Update popup menu

- Add file editor

- Fix android service issues

- Optimize desktop background performance

- Optimize android main process performance

- Optimize delay test

- Optimize vpn protect

- Update changelog

- Update core

- Fix some issues

- Update changelog

- Remake dashboard

- Optimize theme

- Optimize more details

- Update flutter version

- Update changelog

- Support better window position memory

- Add windows arm64 and linux arm64 build script

- Optimize some details

- Remake desktop

- Optimize change proxy

- Optimize network check

- Fix fallback issues

- Optimize lots of details

- Update change.yaml

- Fix android tile issues

- Fix windows tray issues

- Support setting bypassDomain

- Update flutter version

- Fix android service issues

- Fix macos dock exit button issues

- Add route address setting

- Optimize provider view

- Update changelog

- Update CHANGELOG.md

- Add android shortcuts

- Fix init params issues

- Fix dynamic color issues

- Optimize navigator animate

- Optimize window init

- Optimize fab

- Optimize save

- Fix the collapse issues

- Add fontFamily options

- Update core version

- Update flutter version

- Optimize ip check

- Optimize url-test

- Update release message

- Init auto gen changelog

- Fix windows tray issues

- Fix urltest issues

- Add auto changelog

- Fix windows admin auto launch issues

- Add android vpn options

- Support proxies icon configuration

- Optimize android immersion display

- Fix some issues

- Optimize ip detection

- Support android vpn ipv6 inbound switch

- Support log export

- Optimize more details

- Fix android system dns issues

- Optimize dns default option

- Fix some issues

- Update readme

- Fix build error2

- Fix build error

- Support desktop hotkey

- Support android ipv6 inbound

- Support android system dns

- fix some bugs

- Fix delete profile error

- Fix submit error 2

- Fix submit error

- Optimize DNS strategy

- Fix the problem that the tray is not displayed in some cases

- Optimize tray

- Update core

- Fix some error

- Fix tun update issues

- Add DNS override
- Fixed some bugs
- Optimize more detail

- Add Hosts override

- fix android tip error
- fix windows auto launch error

- Fix windows tray issues

- Optimize windows logic

- Optimize app logic

- Support windows administrator auto launch

- Support android close vpn

- Change flutter version

- Support profiles sort

- Support windows country flags display

- Optimize proxies page and profiles page columns

- Update flutter version

- Update version

- Update timeout time

- Update access control page

- Fix bug

- Optimize provider page

- Optimize delay test

- Support local backup and recovery

- Fix android tile service issues

- Fix linux core build error

- Add proxy-only traffic statistics

- Update core

- Optimize more details

- Add fdroid-repo

- Optimize proxies page

- Fix ua issues

- Optimize more details

- Fix windows build error

- Update app icon

- Fix desktop backup error

- Optimize request ua

- Change android icon

- Optimize dashboard

- Remove request validate certificate

- Sync core

- Fix windows error

- Fix setup.dart error

- Fix android system proxy not effective

- Add macos arm64

- Optimize proxies page

- Support mouse drag scroll

- Adjust desktop ui

- Revert "Fix android vpn issues"

- This reverts commit 891977408e6938e2acd74e9b9adb959c48c79988.

- Fix android vpn issues

- Fix android vpn issues

- Rollback partial modification

- Fix the problem that ui can't be synchronized when android vpn is occupied by an external

- Override default socksPort,port

- Fix fab issues

- Update version

- Fix the problem that vpn cannot be started in some cases

- Fix the problem that geodata url does not take effect

- Update ua

- Fix change outbound mode without check ip issues

- Separate android ui and vpn

- Fix url validate issues 2

- Add android hidden from the recent task

- Add geoip file

- Support modify geoData URL

- Fix url validate issues

- Fix check ip performance problem

- Optimize resources page

- Add ua selector

- Support modify test url

- Optimize android proxy

- Fix the error that async proxy provider could not selected the proxy

- Fix android proxy error

- Fix submit error

- Add windows tun

- Optimize android proxy

- Optimize change profile

- Update application ua

- Optimize delay test

- Fix android repeated request notification issues

- Fix memory overflow issues

- Optimize proxies expansion panel 2

- Fix android scan qrcode error

- Optimize proxies expansion panel

- Fix text error

- Optimize proxy

- Optimize delayed sorting performance

- Add expansion panel proxies page

- Support to adjust the proxy card size

- Support to adjust proxies columns number

- Fix autoRun show issues

- Fix Android 10 issues

- Optimize ip show

- Add intranet IP display

- Add connections page

- Add search in connections, requests

- Add keyword search in connections, requests, logs

- Add basic viewing editing capabilities

- Optimize update profile

- Update version

- Fix the problem of excessive memory usage in traffic usage.

- Add lightBlue theme color

- Fix start unable to update profile issues

- Fix flashback caused by process

- Add build version

- Optimize quick start

- Update system default option

- Update build.yml

- Fix android vpn close issues

- Add requests page

- Fix checkUpdate dark mode style error

- Fix quickStart error open app

- Add memory proxies tab index

- Support hidden group

- Optimize logs

- Fix externalController hot load error

- Add tcp concurrent switch

- Add system proxy switch

- Add geodata loader switch

- Add external controller switch

- Add auto gc on trim memory

- Fix android notification error

- Fix ipv6 error

- Fix android udp direct error

- Add ipv6 switch

- Add access all selected button

- Remove android low version splash

- Update version

- Add allowBypass

- Fix Android only pick .text file issues

- Fix search issues

- Fix LoadBalance, Relay load error

- Fix build.yml4

- Fix build.yml3

- Fix build.yml2

- Fix build.yml

- Add search function at access control

- Fix the issues with the profile add button to cover the edit button

- Adapt LoadBalance and Relay

- Add arm

- Fix android notification icon error

- Add one-click update all profiles
- Add expire show

- Temp remove tun mode

- Remove macos in workflow

- Change go version

- Update Version

- Fix tun unable to open

- Optimize delay test2

- Optimize delay test

- Add check ip

- add check ip request

- Fix the problem that the download of remote resources failed after GeodataMode was turned on, which caused the application to flash back.

- Fix edit profile error

- Fix quickStart change proxy error

- Fix core version

- Fix core version

- Update file_picker

- Add resources page

- Optimize more detail

- Add access selected sorted

- Fix notification duplicate creation issue

- Fix AccessControl click issue

- Fix Workflow

- Fix Linux unable to open

- Update README.md 3

- Create LICENSE
- Update README.md 2

- Update README.md

- Optimize workFlow

- optimize checkUpdate

- Fix submit error

- add WebDAV

- add Auto check updates

- Optimize more details

- optimize delayTest

- upgrade flutter version

- Update kernel
- Add import profile via QR code image

- Add compatibility mode and adapt clash scheme.

- update Version

- Reconstruction application proxy logic

- Fix Tab destroy error

- Optimize repeat healthcheck

- Optimize Direct mode ui

- Optimize Healthcheck

- Remove proxies position animation, improve performance
- Add Telegram Link

- Update healthcheck policy

- New Check URLTest

- Fix the problem of invalid auto-selection

- New Async UpdateConfig

- add changeProfileDebounce

- Update Workflow

- Fix ChangeProfile block

- Fix Release Message Error

- Update Selector 2

- Update Version

- Fix Proxies Select Error

- Fix the problem that the proxy group is empty in global mode.

- Fix the problem that the proxy group is empty in global mode.

- Add ProxyProvider2

- Add ProxyProvider

- Update Version

- Update ProxyGroup Sort

- Fix Android quickStart VpnService some problems

- Update version

- Set Android notification low importance

- Fix the issue that VpnService can't be closed correctly in special cases

- Fix the problem that TileService is not destroyed correctly in some cases

- Adjust tab animation defaults

- Add Telegram in README_zh_CN.md

- Add Telegram

- update mobile_scanner

- Initial commit

## v0.8.86

- Fix windows tun issues

- Optimize android get system dns

- Optimize more details

- Update changelog

## v0.8.85

- Support override script

- Support proxies search

- Support svg display

- Optimize config persistence

- Add some scenes auto close connections

- Update core

- Optimize more details

## v0.8.84

- Fix windows service verify issues

- Update changelog

## v0.8.83

- Add windows server mode start process verify

- Add linux deb dependencies

- Add backup recovery strategy select

- Support custom text scaling

- Optimize the display of different text scale

- Optimize windows setup experience

- Optimize startTun performance

- Optimize android tv experience

- Optimize default option

- Optimize computed text size

- Optimize hyperOS freeform window

- Add developer mode

- Update core

- Optimize more details

- Add issues template

- Update changelog

## v0.8.82

- Optimize android vpn performance

- Add custom primary color and color scheme

- Add linux nad windows arm release

- Optimize requests and logs page

- Fix map input page delete issues

- Update changelog

## v0.8.81

- Add rule override

- Update core

- Optimize more details

- Update changelog

## v0.8.80

- Optimize dashboard performance

- Fix some issues

- Fix unselected proxy group delay issues

- Fix asn url issues

- Update changelog

## v0.8.79

- Fix tab delay view issues

- Fix tray action issues

- Fix get profile redirect client ua issues

- Fix proxy card delay view issues

- Add Russian, Japanese adaptation

- Fix some issues

- Update changelog

## v0.8.78

- Fix list form input view issues

- Fix traffic view issues

- Update changelog

## v0.8.77

- Optimize performance

- Update core

- Optimize core stability

- Fix linux tun authority check error

- Fix some issues

- Fix scroll physics error

- Update changelog

## v0.8.75

- Add windows storage corruption detection

- Fix core crash caused by windows resource manager restart

- Optimize logs, requests, access to pages

- Fix macos bypass domain issues

- Update changelog

## v0.8.74

- Fix some issues

- Update changelog

## v0.8.73

- Update popup menu

- Add file editor

- Fix android service issues

- Optimize desktop background performance

- Optimize android main process performance

- Optimize delay test

- Optimize vpn protect

- Update changelog

## v0.8.72

- Update core

- Fix some issues

- Update changelog

## v0.8.71

- Remake dashboard

- Optimize theme

- Optimize more details

- Update flutter version

- Update changelog

## v0.8.70

- Support better window position memory

- Add windows arm64 and linux arm64 build script

- Optimize some details

## v0.8.69

- Remake desktop

- Optimize change proxy

- Optimize network check

- Fix fallback issues

- Optimize lots of details

- Update change.yaml

- Fix android tile issues

- Fix windows tray issues

- Support setting bypassDomain

- Update flutter version

- Fix android service issues

- Fix macos dock exit button issues

- Add route address setting

- Optimize provider view

- Update changelog

- Update CHANGELOG.md

## v0.8.67

- Add android shortcuts

- Fix init params issues

- Fix dynamic color issues

- Optimize navigator animate

- Optimize window init

- Optimize fab

- Optimize save

## v0.8.66

- Fix the collapse issues

- Add fontFamily options

## v0.8.65

- Update core version

- Update flutter version

- Optimize ip check

- Optimize url-test

## v0.8.64

- Update release message

- Init auto gen changelog

- Fix windows tray issues

- Fix urltest issues

- Add auto changelog

- Fix windows admin auto launch issues

- Add android vpn options

- Support proxies icon configuration

- Optimize android immersion display

- Fix some issues

- Optimize ip detection

- Support android vpn ipv6 inbound switch

- Support log export

- Optimize more details

- Fix android system dns issues

- Optimize dns default option

- Fix some issues

- Update readme

## v0.8.60

- Fix build error2

- Fix build error

- Support desktop hotkey

- Support android ipv6 inbound

- Support android system dns

- fix some bugs

## v0.8.59

- Fix delete profile error

## v0.8.58

- Fix submit error 2

- Fix submit error

- Optimize DNS strategy

- Fix the problem that the tray is not displayed in some cases

- Optimize tray

- Update core

- Fix some error

## v0.8.57

- Fix tun update issues

- Add DNS override
- Fixed some bugs
- Optimize more detail

- Add Hosts override

## v0.8.56

- fix android tip error
- fix windows auto launch error

## v0.8.55

- Fix windows tray issues

- Optimize windows logic

- Optimize app logic

- Support windows administrator auto launch

- Support android close vpn

## v0.8.53

- Change flutter version

- Support profiles sort

- Support windows country flags display

- Optimize proxies page and profiles page columns

## v0.8.52

- Update flutter version

- Update version

- Update timeout time

- Update access control page

- Fix bug

## v0.8.51

- Optimize provider page

- Optimize delay test

- Support local backup and recovery

- Fix android tile service issues

## v0.8.49

- Fix linux core build error

- Add proxy-only traffic statistics

- Update core

- Optimize more details

- Merge pull request #140 from txyyh/main

- 添加自建 F-Droid 仓库相关 workflow
- Rename readme fingerprint

- Rename workflow deploy repo name

- Add download guide to README

- Add push release files to fdroid-repo

## v0.8.48

- Optimize proxies page

- Fix ua issues

- Optimize more details

## v0.8.47

- Fix windows build error

## v0.8.46

- Update app icon

- Fix desktop backup error

- Optimize request ua

- Change android icon

- Optimize dashboard

## v0.8.44

- Remove request validate certificate

- Sync core

## v0.8.43

- Fix windows error

## v0.8.42

- Fix setup.dart error

- Fix android system proxy not effective

- Add macos arm64

## v0.8.41

- Optimize proxies page

- Support mouse drag scroll

- Adjust desktop ui

- Revert "Fix android vpn issues"

- This reverts commit 891977408e6938e2acd74e9b9adb959c48c79988.

## v0.8.40

- Fix android vpn issues

- Fix android vpn issues

- Rollback partial modification

## v0.8.39

- Fix the problem that ui can't be synchronized when android vpn is occupied by an external

- Override default socksPort,port

## v0.8.38

- Fix fab issues

## v0.8.37

- Update version

- Fix the problem that vpn cannot be started in some cases

- Fix the problem that geodata url does not take effect

## v0.8.36

- Update ua

- Fix change outbound mode without check ip issues

- Separate android ui and vpn

- Fix url validate issues 2

- Add android hidden from the recent task

- Add geoip file

- Support modify geoData URL

## v0.8.35

- Fix url validate issues

- Fix check ip performance problem

- Optimize resources page

## v0.8.34

- Add ua selector

- Support modify test url

- Optimize android proxy

- Fix the error that async proxy provider could not selected the proxy

## v0.8.33

- Fix android proxy error

- Fix submit error

- Add windows tun

- Optimize android proxy

- Optimize change profile

- Update application ua

- Optimize delay test

## v0.8.32

- Fix android repeated request notification issues

## v0.8.31

- Fix memory overflow issues

## v0.8.30

- Optimize proxies expansion panel 2

- Fix android scan qrcode error

## v0.8.29

- Optimize proxies expansion panel

- Fix text error

## v0.8.28

- Optimize proxy

- Optimize delayed sorting performance

- Add expansion panel proxies page

- Support to adjust the proxy card size

- Support to adjust proxies columns number

- Fix autoRun show issues

- Fix Android 10 issues

- Optimize ip show

## v0.8.26

- Add intranet IP display

- Add connections page

- Add search in connections, requests

- Add keyword search in connections, requests, logs

- Add basic viewing editing capabilities

- Optimize update profile

## v0.8.25

- Update version

- Fix the problem of excessive memory usage in traffic usage.

- Add lightBlue theme color

- Fix start unable to update profile issues

- Fix flashback caused by process

## v0.8.23

- Add build version

- Optimize quick start

- Update system default option

## v0.8.22

- Update build.yml

- Fix android vpn close issues

- Add requests page

- Fix checkUpdate dark mode style error

- Fix quickStart error open app

- Add memory proxies tab index

- Support hidden group

- Optimize logs

- Fix externalController hot load error

## v0.8.21

- Add tcp concurrent switch

- Add system proxy switch

- Add geodata loader switch

- Add external controller switch

- Add auto gc on trim memory

- Fix android notification error

## v0.8.20

- Fix ipv6 error

- Fix android udp direct error

- Add ipv6 switch

- Add access all selected button

- Remove android low version splash

## v0.8.19

- Update version

- Add allowBypass

- Fix Android only pick .text file issues

## v0.8.18

- Fix search issues

## v0.8.17

- Fix LoadBalance, Relay load error

- Fix build.yml4

- Fix build.yml3

- Fix build.yml2

- Fix build.yml

- Add search function at access control

- Fix the issues with the profile add button to cover the edit button

- Adapt LoadBalance and Relay

- Add arm

- Fix android notification icon error

## v0.8.16

- Add one-click update all profiles
- Add expire show

## v0.8.15

- Temp remove tun mode

- Remove macos in workflow

- Change go version

## v0.8.14

- Update Version

- Fix tun unable to open

## v0.8.13

- Optimize delay test2

- Optimize delay test

- Add check ip

- add check ip request

## v0.8.12

- Fix the problem that the download of remote resources failed after GeodataMode was turned on, which caused the
  application to flash back.

- Fix edit profile error

- Fix quickStart change proxy error

- Fix core version

## v0.8.10

- Fix core version

## v0.8.9

- Update file_picker

- Add resources page

- Optimize more detail

- Add access selected sorted

- Fix notification duplicate creation issue

- Fix AccessControl click issue

## v0.8.7

- Fix Workflow

- Fix Linux unable to open

- Update README.md 3

- Create LICENSE
- Update README.md 2

- Update README.md

- Optimize workFlow

## v0.8.6

- optimize checkUpdate

## v0.8.5

- Fix submit error

## v0.8.4

- add WebDAV

- add Auto check updates

- Optimize more details

- optimize delayTest

## v0.8.2

- upgrade flutter version

## v0.8.1

- Update kernel
- Add import profile via QR code image

## v0.8.0

- Add compatibility mode and adapt clash scheme.

## v0.7.14

- update Version

- Reconstruction application proxy logic

## v0.7.13

- Fix Tab destroy error

## v0.7.12

- Optimize repeat healthcheck

## v0.7.11

- Optimize Direct mode ui

## v0.7.10

- Optimize Healthcheck

- Remove proxies position animation, improve performance
- Add Telegram Link

- Update healthcheck policy

- New Check URLTest

- Fix the problem of invalid auto-selection

## v0.7.8

- New Async UpdateConfig

- add changeProfileDebounce

- Update Workflow

- Fix ChangeProfile block

- Fix Release Message Error

## v0.7.7

- Update Selector 2

## v0.7.6

- Update Version

- Fix Proxies Select Error

## v0.7.5

- Fix the problem that the proxy group is empty in global mode.

- Fix the problem that the proxy group is empty in global mode.

## v0.7.4

- Add ProxyProvider2

## v0.7.3

- Add ProxyProvider

- Update Version

- Update ProxyGroup Sort

- Fix Android quickStart VpnService some problems

## v0.7.1

- Update version

- Set Android notification low importance

- Fix the issue that VpnService can't be closed correctly in special cases

- Fix the problem that TileService is not destroyed correctly in some cases

- Adjust tab animation defaults

- Add Telegram in README_zh_CN.md

- Add Telegram

## v0.7.0

- update mobile_scanner

- Initial commit