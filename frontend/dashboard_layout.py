import os
import dash
from dash import html, page_container
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output
from config.settings import PROJECT_INFO
from dash import callback_context

DOCS_FOLDER = "api/docs"

dashboard_layout  = html.Main([

    # Cabeçalho
    html.Header([
        html.Img(src="/assets/logo.png", className="logo", alt="Logo OpsLinux"),
        html.Span("OpsLinux")
    ], className="navbar"),

    # Layout principal
    html.Section([

        # Barra lateral (nav)
        html.Aside([
            html.Span(className="span-space"),
            html.Nav([
                html.A([
                    html.I(className="bi bi-bar-chart"),
                    html.Span("Dashboard", className="tooltip-text")
                ], href="/", className="sidebar-item item-dash"),

                html.A([
                    html.I(className="bi bi-file-earmark-text"),
                    html.Span("Docs", className="tooltip-text")
                ], href="/doc", className="sidebar-item"),

                html.A([
                    html.I(className="bi bi-info-circle"),
                    html.Span("Info", className="tooltip-text")
                ], href="#", className="sidebar-item"),
            ], className="sidebar")
        ]),

        # Conteúdo dinâmico baseado na página acessada
        html.Article([
            page_container
        ], className="page_container_dash"),
    ], className="main-content")
])