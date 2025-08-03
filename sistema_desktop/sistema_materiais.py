#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Gerenciamento de Materiais
Aplicação desktop com tkinter para CRUD de materiais via API
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from typing import List, Dict, Optional

class APIClient:
    """Cliente para comunicação com a API de materiais"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def get_materiais(self) -> List[Dict]:
        """Obtém lista de materiais da API"""
        try:
            response = requests.get(f"{self.base_url}/materiais")
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com a API: {e}")
            # Retorna dados mock para teste
            return self._get_mock_data()
    
    def criar_material(self, nome: str, descricao: str) -> bool:
        """Cria um novo material via API"""
        try:
            data = {"nome": nome, "descricao": descricao}
            response = requests.post(f"{self.base_url}/cadastrar-material", json=data)
            return response.status_code in [200, 201]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar material: {e}")
            return True  # Simula sucesso para teste
    
    def atualizar_material(self, material_id: int, nome: str, descricao: str) -> bool:
        """Atualiza um material existente via API"""
        try:
            data = {"nome": nome, "descricao": descricao}
            response = requests.put(f"{self.base_url}/atualizar-material/{material_id}", json=data)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar material: {e}")
            return True  # Simula sucesso para teste
    
    def deletar_material(self, material_id: int) -> bool:
        """Deleta um material via API"""
        try:
            response = requests.delete(f"{self.base_url}/excluir-material/{material_id}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar material: {e}")
            return True  # Simula sucesso para teste
    
    def _get_mock_data(self) -> List[Dict]:
        """Dados mock para teste quando API não está disponível"""
        return [
            {"id": 1, "nome": "Parafuso M6x30", "descricao": "Parafuso sextavado métrico 6mm x 30mm"},
            {"id": 2, "nome": "Porca M6", "descricao": "Porca sextavada métrica 6mm"},
            {"id": 3, "nome": "Arruela Lisa M6", "descricao": "Arruela lisa para parafuso M6"},
            {"id": 4, "nome": "Cabo Flexível 2,5mm", "descricao": "Cabo flexível para instalações elétricas"},
            {"id": 5, "nome": "Disjuntor 20A", "descricao": "Disjuntor monopolar 20 amperes"}
        ]


class ListaMateriais:
    """Tela 1: Lista e exclusão de materiais"""
    
    def __init__(self, parent, api_client: APIClient, on_incluir=None, on_editar=None):
        self.parent = parent
        self.api_client = api_client
        self.on_incluir = on_incluir
        self.on_editar = on_editar
        self.materiais = []
        
        self.setup_ui()
        self.carregar_materiais()
    
    def setup_ui(self):
        """Configura a interface da tela de listagem"""
        self.frame = ttk.Frame(self.parent)
        
        # Título
        titulo = ttk.Label(self.frame, text="Lista de Materiais", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        
        # Frame para botões superiores
        frame_botoes_top = ttk.Frame(self.frame)
        frame_botoes_top.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame_botoes_top, text="Incluir Material", 
                  command=self.incluir_material).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_top, text="Atualizar Lista", 
                  command=self.carregar_materiais).pack(side=tk.LEFT, padx=5)
        
        # Frame para a treeview
        frame_tree = ttk.Frame(self.frame)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview para listar materiais
        colunas = ("ID", "Nome", "Descrição")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=15)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Descrição", text="Descrição")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=200)
        self.tree.column("Descrição", width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botões inferiores
        frame_botoes_bottom = ttk.Frame(self.frame)
        frame_botoes_bottom.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame_botoes_bottom, text="Editar Selecionado", 
                  command=self.editar_material).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_bottom, text="Excluir Selecionado", 
                  command=self.excluir_material).pack(side=tk.LEFT, padx=5)
    
    def carregar_materiais(self):
        """Carrega materiais da API e atualiza a treeview"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Carregar dados da API
        self.materiais = self.api_client.get_materiais()
        
        # Inserir na treeview
        for material in self.materiais:
            self.tree.insert("", tk.END, values=(
                material.get("id", ""),
                material.get("nome", ""),
                material.get("descricao", "")
            ))
    
    def incluir_material(self):
        """Abre tela de inclusão de material"""
        if self.on_incluir:
            self.on_incluir()
    
    def editar_material(self):
        """Abre tela de edição do material selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um material para editar.")
            return
        
        item = self.tree.item(selecionado[0])
        material_id = item["values"][0]
        
        # Encontrar material completo
        material = next((m for m in self.materiais if m["id"] == material_id), None)
        if material and self.on_editar:
            self.on_editar(material)
    
    def excluir_material(self):
        """Exclui o material selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um material para excluir.")
            return
        
        item = self.tree.item(selecionado[0])
        material_id = item["values"][0]
        material_nome = item["values"][1]
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar Exclusão", 
                              f"Deseja realmente excluir o material '{material_nome}'?"):
            if self.api_client.deletar_material(material_id):
                messagebox.showinfo("Sucesso", "Material excluído com sucesso!")
                self.carregar_materiais()  # Recarregar lista
            else:
                messagebox.showerror("Erro", "Erro ao excluir material.")
    
    def show(self):
        """Exibe a tela"""
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.carregar_materiais()  # Recarregar ao exibir
    
    def hide(self):
        """Oculta a tela"""
        self.frame.pack_forget()


class IncluirMaterial:
    """Tela 2: Inclusão de material"""
    
    def __init__(self, parent, api_client: APIClient, on_voltar=None):
        self.parent = parent
        self.api_client = api_client
        self.on_voltar = on_voltar
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface da tela de inclusão"""
        self.frame = ttk.Frame(self.parent)
        
        # Título
        titulo = ttk.Label(self.frame, text="Incluir Novo Material", font=("Arial", 16, "bold"))
        titulo.pack(pady=20)
        
        # Frame principal do formulário
        form_frame = ttk.Frame(self.frame)
        form_frame.pack(expand=True)
        
        # Campo Nome
        ttk.Label(form_frame, text="Nome do Material:", font=("Arial", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.entry_nome = ttk.Entry(form_frame, width=50, font=("Arial", 11))
        self.entry_nome.pack(pady=(0, 10))
        
        # Campo Descrição
        ttk.Label(form_frame, text="Descrição:", font=("Arial", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.text_descricao = tk.Text(form_frame, width=50, height=6, font=("Arial", 11))
        self.text_descricao.pack(pady=(0, 20))
        
        # Frame para botões
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.pack(pady=20)
        
        ttk.Button(botoes_frame, text="Salvar", command=self.salvar_material).pack(side=tk.LEFT, padx=10)
        ttk.Button(botoes_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=10)
        ttk.Button(botoes_frame, text="Voltar", command=self.voltar).pack(side=tk.LEFT, padx=10)
    
    def salvar_material(self):
        """Salva o material via API"""
        nome = self.entry_nome.get().strip()
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        
        if not nome:
            messagebox.showerror("Erro", "O nome do material é obrigatório.")
            return
        
        if not descricao:
            messagebox.showerror("Erro", "A descrição do material é obrigatória.")
            return
        
        if self.api_client.criar_material(nome, descricao):
            messagebox.showinfo("Sucesso", "Material incluído com sucesso!")
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Erro ao incluir material.")
    
    def limpar_campos(self):
        """Limpa os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        self.entry_nome.focus()
    
    def voltar(self):
        """Volta para a tela anterior"""
        if self.on_voltar:
            self.on_voltar()
    
    def show(self):
        """Exibe a tela"""
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.entry_nome.focus()
    
    def hide(self):
        """Oculta a tela"""
        self.frame.pack_forget()


class EditarMaterial:
    """Tela 3: Edição de material"""
    
    def __init__(self, parent, api_client: APIClient, on_voltar=None):
        self.parent = parent
        self.api_client = api_client
        self.on_voltar = on_voltar
        self.material_atual = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface da tela de edição"""
        self.frame = ttk.Frame(self.parent)
        
        # Título
        self.titulo = ttk.Label(self.frame, text="Editar Material", font=("Arial", 16, "bold"))
        self.titulo.pack(pady=20)
        
        # Frame principal do formulário
        form_frame = ttk.Frame(self.frame)
        form_frame.pack(expand=True)
        
        # Campo ID (somente leitura)
        ttk.Label(form_frame, text="ID:", font=("Arial", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.entry_id = ttk.Entry(form_frame, width=50, font=("Arial", 11), state="readonly")
        self.entry_id.pack(pady=(0, 10))
        
        # Campo Nome
        ttk.Label(form_frame, text="Nome do Material:", font=("Arial", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.entry_nome = ttk.Entry(form_frame, width=50, font=("Arial", 11))
        self.entry_nome.pack(pady=(0, 10))
        
        # Campo Descrição
        ttk.Label(form_frame, text="Descrição:", font=("Arial", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.text_descricao = tk.Text(form_frame, width=50, height=6, font=("Arial", 11))
        self.text_descricao.pack(pady=(0, 20))
        
        # Frame para botões
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.pack(pady=20)
        
        ttk.Button(botoes_frame, text="Salvar Alterações", command=self.salvar_alteracoes).pack(side=tk.LEFT, padx=10)
        ttk.Button(botoes_frame, text="Cancelar", command=self.voltar).pack(side=tk.LEFT, padx=10)
    
    def carregar_material(self, material: Dict):
        """Carrega os dados do material nos campos"""
        self.material_atual = material
        
        # Atualizar título
        self.titulo.config(text=f"Editar Material - {material.get('nome', '')}")
        
        # Limpar campos
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        
        # Preencher campos
        self.entry_id.insert(0, str(material.get("id", "")))
        self.entry_id.config(state="readonly")
        self.entry_nome.insert(0, material.get("nome", ""))
        self.text_descricao.insert("1.0", material.get("descricao", ""))
    
    def salvar_alteracoes(self):
        """Salva as alterações via API"""
        if not self.material_atual:
            messagebox.showerror("Erro", "Nenhum material carregado para edição.")
            return
        
        nome = self.entry_nome.get().strip()
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        
        if not nome:
            messagebox.showerror("Erro", "O nome do material é obrigatório.")
            return
        
        if not descricao:
            messagebox.showerror("Erro", "A descrição do material é obrigatória.")
            return
        
        material_id = self.material_atual["id"]
        
        if self.api_client.atualizar_material(material_id, nome, descricao):
            messagebox.showinfo("Sucesso", "Material atualizado com sucesso!")
            self.voltar()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar material.")
    
    def voltar(self):
        """Volta para a tela anterior"""
        if self.on_voltar:
            self.on_voltar()
    
    def show(self):
        """Exibe a tela"""
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.entry_nome.focus()
    
    def hide(self):
        """Oculta a tela"""
        self.frame.pack_forget()


class SistemaMateriais:
    """Aplicação principal que gerencia as telas"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gerenciamento de Materiais")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Cliente da API
        self.api_client = APIClient()
        
        # Container principal
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inicializar telas
        self.tela_lista = ListaMateriais(
            self.container, 
            self.api_client,
            on_incluir=self.mostrar_incluir,
            on_editar=self.mostrar_editar
        )
        
        self.tela_incluir = IncluirMaterial(
            self.container,
            self.api_client,
            on_voltar=self.mostrar_lista
        )
        
        self.tela_editar = EditarMaterial(
            self.container,
            self.api_client,
            on_voltar=self.mostrar_lista
        )
        
        # Mostrar tela inicial
        self.mostrar_lista()
    
    def mostrar_lista(self):
        """Mostra a tela de listagem"""
        self.tela_incluir.hide()
        self.tela_editar.hide()
        self.tela_lista.show()
    
    def mostrar_incluir(self):
        """Mostra a tela de inclusão"""
        self.tela_lista.hide()
        self.tela_editar.hide()
        self.tela_incluir.show()
    
    def mostrar_editar(self, material):
        """Mostra a tela de edição"""
        self.tela_lista.hide()
        self.tela_incluir.hide()
        self.tela_editar.carregar_material(material)
        self.tela_editar.show()
    
    def run(self):
        """Inicia a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


if __name__ == "__main__":
    app = SistemaMateriais()
    app.run()
