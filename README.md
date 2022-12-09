<h1>Приложение IVA-R-Dashboard</h1>

Created by pavelbeard

Введение:
  <ul>
    <li><a href="#from-which-includes">Из чего состоит?</a></li>
    <li>Как установить?</li>
    <li>Как пользоваться?</li>
  </ul>

<div id="from-which-includes">
    <h2>Из чего состоит?</h2>
    <p>Приложение состоит из 4 частей:</p>
    <ol>
        <li>Агент мониторинга</li>
        <li>Сервер инфопанели</li>
        <li>База данных</li>
        <li>Скрипт, создающий файл known_hosts</li>
    </ol>
    <br>
    <p>Само приложение контейнеризировано, состоит из независимых сервисов,<br>
    хотя скрипт не является таковым, но ему уделю отдельное внимание</p>
    <p style="text-align: center">Начнем с <b>Агента мониторинга!</b><br>
    Он включает в себя мегапакет <b>core</b>, который, в свою очередь состоит
    из пакетов:</p>
    <ul>
        <li><b>handlers</b></li>
        <li><b>routers</b></li>
        <li><b>ssh_client</b></li>
    </ul>
    <p>Также в состав пакета <b>core</b> входят модули:</p>
    <ul>
        <li><b><i>core</i></b></li>
        <li><b><i>decorators</i></b></li>
        <li><b><i>exceptions</i></b></li>
        <li><b><i>tests</i></b></li>
    </ul>
    <p>Примерная структура сервиса в версии приложения <b>v0.0.1</b> выглядит так:</p>
    <img src="doc_pics/project_structure.png" 
        alt="project_structure" width="300" height="400"/>

</div>