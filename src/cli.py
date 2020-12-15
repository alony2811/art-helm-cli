import argparse
import subprocess
import os

class Actions(object):
    def __init__(self,version='None', max_db_con='None', license_path='None'):
        self.version = version
        self.max_db_con = max_db_con
        self.license_path = license_path
        return

    def install(self):
        # Adding chartCenter helm repository and update your repo
        subprocess.call(["echo Adding ChartCenter helm repository"], shell=True)
        subprocess.call(["helm repo add center https://repo.chartcenter.io"], shell=True)
        subprocess.call(["helm repo update"], shell=True)
        # Create artifactory namespace
        subprocess.call(["echo Create artifactory namespace"], shell=True)
        subprocess.call(["kubectl create namespace artifactory"], shell=True)
        # Deploy artifactory
        cmd = "helm upgrade --install artifactory --namespace artifactory center/jfrog/artifactory " + \
              "--set postgresql.enabled=false"
        if self.version is not None:
            cmd = cmd + " --set artifactory.image.tag="+self.version
        if self.max_db_con is not None:
            cmd = cmd + " --set artifactory.database.maxOpenConnections="+self.max_db_con
        if self.license_path is not None:
            # Create the kubernetes secret (assuming the local license file)
            subprocess.call(["kubectl -n artifactory create secret generic artifactory-license --from-file=" +
                             self.license_path], shell=True)
            # Get the license name from the license path
            license_path, license_name = os.path.split(self.license_path)
            cmd = cmd + " --set artifactory.license.secret=artifactory-license,artifactory.license.dataKey=" + \
                        license_name
        subprocess.call(["echo Install artifactory helm chart"], shell=True)
        #helm upgrade --install artifactory --set postgresql.enabled=false --namespace artifactory center/jfrog/artifactory
        try:
            subprocess.call('echo '+cmd, shell=True)
            subprocess.call(cmd, shell=True)
        except:
            subprocess.call(["echo Artifactory helm chart installation encountered in error!"], shell=True)
        else:
            subprocess.call(["echo Artifactory helm chart installed successfully!"], shell=True)
            subprocess.call(["echo ----------------------------------------------"], shell=True)
            subprocess.call(["echo Please wait few minutes for the deployment to be done!"], shell=True)
            subprocess.call(["echo You can watch the pods status with \'kubectl get pods -n artifactory\' "
                             "command"], shell=True)
            subprocess.call(["echo Once all the pod running you can lunch to Artifactory with \' minikube -n "
                             "artifactory service artifactory-artifactory --url\' command"], shell=True)
            subprocess.call(["echo ----------------------------------------------"], shell=True)

        return

    def delete(self):
        subprocess.call(["echo Delete artifactory namespace"], shell=True)
        subprocess.call(["kubectl delete namespace artifactory"], shell=True)
        subprocess.call(["echo Artifactory helm chart deleted successfully!"], shell=True)
        return



def main():
    parser = argparse.ArgumentParser(description='CLI deploying artifactory latest chart with override params',
                                     epilog='Enjoy the program! :)')
    parser.add_argument('command', choices=['install','delete'], help = 'actions can be perform')
    parser.add_argument('-v','--version', type=str, default=None, help = 'artifactory version number, e.g: '
                                                                         '7.11.2, 7.10.6,')
    parser.add_argument('-md','--dbmax', type=str, default= None, help = 'DB max connection')
    parser.add_argument('-l','--license', type=str, default=None, help = 'license file path, e.g: ./art-lic')
    args = parser.parse_args()


    if args.command == 'install':
        print(args)
        actions = Actions(version=args.version, max_db_con=args.dbmax, license_path=args.license)
        actions.install()

    if args.command == 'delete':
        actions = Actions()
        actions.delete()

if __name__ == '__main__':
    main()