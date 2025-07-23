# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


class StaticPageAPI:
    """
    静态页面API服务类
    用于为FastAPI应用添加前端静态资源服务功能
    """
    
    def __init__(self, app: FastAPI, frontend_dist_path: Optional[str] = None):
        """
        初始化静态页面API服务
        
        Args:
            app: FastAPI应用实例
            frontend_dist_path: 前端构建文件路径，默认为项目根目录下的frontend/dist
        """
        self.app = app
        self.project_root = Path(__file__).parent.parent
        
        # 设置前端构建文件路径
        if frontend_dist_path:
            self.frontend_dist_path = Path(frontend_dist_path)
        else:
            self.frontend_dist_path = self.project_root / "frontend" / "dist"
        
        # 检查前端构建文件是否存在
        self.frontend_available = self._check_frontend_files()
        
        # 如果前端文件可用，则配置静态文件服务
        if self.frontend_available:
            self._setup_static_files()
            self._setup_spa_routes()
        
        # 添加静态服务状态检查端点
        self._setup_status_endpoint()
    
    def _check_frontend_files(self) -> bool:
        """
        检查前端构建文件是否存在
        
        Returns:
            bool: 前端文件是否可用
        """
        try:
            # 检查dist目录是否存在
            if not self.frontend_dist_path.exists():
                print(f"前端构建目录不存在: {self.frontend_dist_path}")
                return False
            
            # 检查index.html是否存在
            index_file = self.frontend_dist_path / "index.html"
            if not index_file.exists():
                print(f"前端入口文件不存在: {index_file}")
                return False
            
            # 检查assets目录是否存在
            assets_dir = self.frontend_dist_path / "assets"
            if not assets_dir.exists():
                print(f"前端资源目录不存在: {assets_dir}")
                return False
            
            print(f"前端构建文件检查通过: {self.frontend_dist_path}")
            return True
            
        except Exception as e:
            print(f"检查前端文件时发生错误: {e}")
            return False
    
    def _setup_static_files(self):
        """
        配置静态文件服务
        """
        try:
            # 挂载assets静态资源目录
            assets_path = self.frontend_dist_path / "assets"
            if assets_path.exists():
                self.app.mount(
                    "/assets",
                    StaticFiles(directory=str(assets_path)),
                    name="assets"
                )
                print(f"已挂载静态资源目录: /assets -> {assets_path}")
            
            # 挂载其他静态文件（如favicon、图标等）
            for static_file in ["logo.svg", "favicon.ico", "favicon.png"]:
                file_path = self.frontend_dist_path / static_file
                if file_path.exists():
                    @self.app.get(f"/{static_file}")
                    async def serve_static_file(file_name=static_file):
                        return FileResponse(self.frontend_dist_path / file_name)
            
        except Exception as e:
            print(f"配置静态文件服务时发生错误: {e}")
    
    def _setup_spa_routes(self):
        """
        配置SPA（单页应用）路由
        为前端路由提供index.html文件服务
        """
        try:
            index_file = self.frontend_dist_path / "index.html"
            
            # 为前端路由提供SPA支持
            # 这些路径应该返回index.html，让前端路由器处理
            frontend_routes = [
                "/intro",
                "/dashboard"
            ]
            
            # 为每个前端路由创建处理函数
            def create_spa_handler(index_path):
                async def serve_spa_route():
                    """服务SPA路由"""
                    return FileResponse(index_path)
                return serve_spa_route
            
            for route in frontend_routes:
                # 注册精确路径
                self.app.get(route, response_class=HTMLResponse, include_in_schema=False)(create_spa_handler(index_file))
                # 注册子路径（包括多级路径）
                self.app.get(f"{route}/{{path:path}}", response_class=HTMLResponse, include_in_schema=False)(create_spa_handler(index_file))
            
            print("已配置SPA路由支持")
            
        except Exception as e:
            print(f"配置SPA路由时发生错误: {e}")
    
    def _setup_status_endpoint(self):
        """
        设置静态服务状态检查端点
        """
        @self.app.get("/static/status", summary="静态文件服务状态")
        async def static_service_status():
            """获取静态文件服务状态"""
            return {
                "frontend_available": self.frontend_available,
                "frontend_dist_path": str(self.frontend_dist_path),
                "index_file_exists": (self.frontend_dist_path / "index.html").exists() if self.frontend_available else False,
                "assets_dir_exists": (self.frontend_dist_path / "assets").exists() if self.frontend_available else False,
                "message": "前端静态文件服务正常" if self.frontend_available else "前端构建文件不可用，请先构建前端项目"
            }
    
    def setup_cors(self, 
                   allow_origins: list = None,
                   allow_credentials: bool = True,
                   allow_methods: list = None,
                   allow_headers: list = None):
        """
        配置CORS中间件
        
        Args:
            allow_origins: 允许的源列表
            allow_credentials: 是否允许凭据
            allow_methods: 允许的HTTP方法列表
            allow_headers: 允许的请求头列表
        """
        if allow_origins is None:
            allow_origins = ["*"]
        if allow_methods is None:
            allow_methods = ["*"]
        if allow_headers is None:
            allow_headers = ["*"]
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )
        print("已配置CORS中间件")


def setup_static_page_api(app: FastAPI, frontend_dist_path: Optional[str] = None) -> StaticPageAPI:
    """
    为FastAPI应用设置静态页面API服务的便捷函数
    
    Args:
        app: FastAPI应用实例
        frontend_dist_path: 前端构建文件路径，默认为项目根目录下的frontend/dist
    
    Returns:
        StaticPageAPI: 静态页面API服务实例
    
    Example:
        ```python
        from fastapi import FastAPI
        from static_page_api import setup_static_page_api
        
        app = FastAPI()
        
        # 设置静态页面服务
        static_api = setup_static_page_api(app)
        
        # 可选：配置CORS
        static_api.setup_cors()
        ```
    """
    return StaticPageAPI(app, frontend_dist_path)


def create_integrated_app(api_app: FastAPI, frontend_dist_path: Optional[str] = None) -> FastAPI:
    """
    创建集成了静态文件服务的FastAPI应用
    
    Args:
        api_app: 现有的API应用实例
        frontend_dist_path: 前端构建文件路径
    
    Returns:
        FastAPI: 集成了静态文件服务的应用实例
    """
    # 设置静态页面服务
    static_api = setup_static_page_api(api_app, frontend_dist_path)
    
    # 配置CORS以支持前后端集成
    static_api.setup_cors(
        allow_origins=["*"],  # 在生产环境中应该限制具体的域名
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"]
    )
    
    # 在所有API路由注册完成后，添加根路径和fallback路由
    if static_api.frontend_available:
        index_file = static_api.frontend_dist_path / "index.html"
        
        # 根路径返回index.html
        @api_app.get("/", response_class=HTMLResponse, include_in_schema=False)
        async def serve_frontend_root():
            """服务前端根页面"""
            return FileResponse(index_file)
        
        # 添加通用的SPA路由处理器（作为最后的fallback）
        # 这将捕获所有不匹配API路由和静态资源的请求
        @api_app.get("/{path:path}", response_class=HTMLResponse, include_in_schema=False)
        async def serve_spa_fallback(path: str):
            """SPA fallback路由 - 处理所有未匹配的路径"""
            # 排除API路径和静态资源路径
            if (path.startswith("api/") or 
                path.startswith("assets/") or 
                path.startswith("static/") or
                path.startswith("docs") or
                path.startswith("openapi.json") or
                path.startswith("redoc")):
                from fastapi import HTTPException
                raise HTTPException(status_code=404, detail="Not Found")
            return FileResponse(index_file)
        
        print("已添加根路径和SPA fallback路由")
    
    return api_app