package ca.utoronto.utsc.dagger2;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;

//a module, which is a class that provides or builds the objects’ dependencies
//A Module class is annotated with the @Module annotation,
//indicating that it can make dependencies available to the container.
//Then, we need to add the @Provides annotation on methods that construct our dependencies

@Module
public class VehiclesModule {

	@Provides
	public Engine provideEngine() {
		return new Engine();
	}

	@Provides
	@Singleton
	public Brand provideBrand() {
		return new Brand("CSCC01");
	}
}
