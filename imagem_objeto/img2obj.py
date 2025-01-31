import os
import vtk

def vizualizar_modelo(nomeObjeto):
    # Le o arquivo.obj
    reader = vtk.vtkOBJReader()
    reader.SetFileName(f"objetos/{nomeObjeto}")
    reader.Update()

    # mapper e ator para o modelo
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # renderiza
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # iniciar visualização
    render_window.Render()
    render_window_interactor.Start()

def converter(caminho_img, nome_objeto, diretorio_objeto):
    diretorio_modelo = "ailia-models/neural_rendering/tripo_sr/"
    pre_diretorio_modelo = './imagem_objeto/'
    print(f"pre_diretorio_modelo: {pre_diretorio_modelo}")
    print(f"Caminho da imagem: {caminho_img}")
    print(f"copiando de {caminho_img} para {pre_diretorio_modelo}/{diretorio_modelo}input.png")
    os.system(f"cp {caminho_img} {pre_diretorio_modelo}/{diretorio_modelo}input.png")
    print(f"executando o comando cd {pre_diretorio_modelo}/{diretorio_modelo}&& python3 tripo_sr.py --savepath {diretorio_objeto}/{nome_objeto}.obj")
    os.system(f"cd {pre_diretorio_modelo}/{diretorio_modelo}&& python3 tripo_sr.py --savepath ../../../../{diretorio_objeto}/{nome_objeto}.obj")


def main():
    opcao = int(input("1 -> Converter imagem para objeto 3D\n2 -> Vizualizar um Objeto 3D  "))
    if opcao == 1:
        nome_img = 'foo'# input("Nome da imagem: ")
        #caminho_img = input("Caminho da imagem: ")
        #nome_objeto = input("Caminho do objeto: ")
        caminho_img = "../static/uploads/1/arvi.png"
        nome_objeto = "arvi.obj"
        converter(caminho_img, nome_objeto)
        opcao = int(input("Deseja vizualizar o objeto? (1-Sim/2-Não)"))
        if opcao == 1:
            vizualizar_modelo(nome_objeto)
    elif opcao == 2:
        nome_objeto = input("Nome do objeto: ")
        vizualizar_modelo(nome_objeto)

if __name__ == "__main__":
    main()