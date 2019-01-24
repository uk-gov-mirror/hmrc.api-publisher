/*
 * Copyright 2019 HM Revenue & Customs
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package uk.gov.hmrc.apipublisher.config

import com.google.inject.{AbstractModule, Provides}
import play.api.Mode.Mode
import play.api.{Configuration, Environment, Play}
import uk.gov.hmrc.apipublisher.connectors.{DocumentationRamlLoader, DocumentationUrlRewriter}
import uk.gov.hmrc.play.config.ServicesConfig
import uk.gov.hmrc.ramltools.loaders.{RamlLoader, UrlRewriter}
import javax.inject.Singleton

class Module (environment: Environment, configuration: Configuration) extends AbstractModule {

  @Provides
  @Singleton
  def servicesConfig: ServicesConfig = new ServicesConfig {
    override protected def mode: Mode = Play.current.mode
    override protected def runModeConfiguration: Configuration = Play.current.configuration
  }

  override def configure(): Unit = {
    bind(classOf[UrlRewriter]).to(classOf[DocumentationUrlRewriter])
    bind(classOf[RamlLoader]).to(classOf[DocumentationRamlLoader])
    bind(classOf[WSHttp]).toInstance(AuditedWSHttp)
  }
}
